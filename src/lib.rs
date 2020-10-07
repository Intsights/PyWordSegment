use pyo3::prelude::*;
use std::cmp;
use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

const MAX_WORD_LEN: usize = 24;

#[pyclass]
#[text_signature = "(unigrams_file_path, bigrams_file_path, total_words_frequency, /)"]
#[derive(Default)]
struct WordSegmenter {
    unigrams: HashMap<String, f64>,
    bigrams: HashMap<String, f64>,
    total_words_frequency: f64,
}

#[pymethods]
impl WordSegmenter {
    #[new]
    fn new(
        unigrams_file_path: &str,
        bigrams_file_path: &str,
        total_words_frequency: f64,
    ) -> Self {
        let mut unigrams = HashMap::new();
        let unigrams_file = File::open(unigrams_file_path).unwrap();
        let unigrams_file_buf_reader = BufReader::new(unigrams_file);
        for line in unigrams_file_buf_reader.lines() {
            let line = line.unwrap();
            let splitted_line: Vec<&str> = line.split('\t').collect();
            let word = splitted_line.get(0).unwrap().to_string();
            let frequency = splitted_line.get(1).unwrap().parse().unwrap();
            unigrams.insert(word, frequency);
        }

        let mut bigrams = HashMap::new();
        let bigrams_file = File::open(bigrams_file_path).unwrap();
        let bigrams_file_buf_reader = BufReader::new(bigrams_file);
        for line in bigrams_file_buf_reader.lines() {
            let line = line.unwrap();
            let splitted_line: Vec<&str> = line.split('\t').collect();
            let word = splitted_line.get(0).unwrap().to_string();
            let frequency = splitted_line.get(1).unwrap().parse().unwrap();
            bigrams.insert(word, frequency);
        }

        WordSegmenter {
            unigrams,
            bigrams,
            total_words_frequency,
        }
    }

    #[text_signature = "(text, /)"]
    fn segment(
        &self,
        py: Python,
        text: String,
    ) -> PyResult<Py<PyAny>> {
        let mut memo = HashMap::with_capacity(500);
        let clean_text = text
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );
        let (_score, words) = self.search(&mut memo, &clean_text, "<s>");

        Ok(words.into_py(py))
    }

    #[text_signature = "(substring, text, /)"]
    fn exist_as_segment(
        &self,
        substring: String,
        text: String,
    ) -> PyResult<bool> {
        let mut memo = HashMap::with_capacity(500);
        let clean_text = text
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );
        let (_score, segmented_text) = self.search(&mut memo, &clean_text, "<s>");

        let mut memo = HashMap::with_capacity(500);
        let clean_substring = substring
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );
        let (_score, segmented_substring) = self.search(&mut memo, &clean_substring, "<s>");

        let segmented_substring_pattern = format!("-{}-", segmented_substring.join("-"));
        let segmented_text_pattern = format!("-{}-", segmented_text.join("-"));

        Ok(segmented_text_pattern.contains(&segmented_substring_pattern))
    }
}

impl WordSegmenter {
    fn score(
        &self,
        word: &str,
        previous: &str,
    ) -> f64 {
        if self.unigrams.contains_key(previous) {
            let bigram = format!("{} {}", previous, word);
            if let Some(bigram_frequency) = self.bigrams.get(&bigram) {
                return bigram_frequency / self.unigrams.get(previous).unwrap();
            }
        }
        match self.unigrams.get(word) {
            Some(frequency) => frequency / self.total_words_frequency,
            None => 10.0 / (self.total_words_frequency * 10_f64.powi(word.len() as i32)),
        }
    }

    fn search<'a>(
        &self,
        memo: &mut HashMap<(&'a str, &'a str), (f64, Vec<&'a str>)>,
        text: &'a str,
        previous: &str,
    ) -> (f64, Vec<&'a str>) {
        let mut best_candidate = (-100000.0, Vec::new());
        for pos in 1..cmp::min(text.len(), MAX_WORD_LEN) + 1 {
            let prefix = &text[..pos];
            let suffix = &text[pos..];
            let prefix_score = self.score(prefix, previous).log10();

            if let Some((suffix_score, suffix_words)) = memo.get(&(suffix, prefix)) {
                if best_candidate.0 < prefix_score + suffix_score {
                    let mut suffix_words = suffix_words.clone();
                    suffix_words.insert(0, prefix);
                    best_candidate = (prefix_score + suffix_score, suffix_words);
                }
            } else {
                if suffix.is_empty() {
                    if best_candidate.0 < prefix_score {
                        best_candidate = (prefix_score, vec![prefix]);
                    }
                    memo.insert((suffix, prefix), (0.0, Vec::new()));
                } else {
                    let (suffix_score, suffix_words) = self.search(memo, suffix, prefix);
                    if best_candidate.0 < prefix_score + suffix_score {
                        let mut suffix_words = suffix_words.clone();
                        suffix_words.insert(0, prefix);
                        best_candidate = (prefix_score + suffix_score, suffix_words);
                    }
                    memo.insert((suffix, prefix), (suffix_score, suffix_words));
                }
            }
        }

        best_candidate
    }
}

#[pymodule]
fn pywordsegment(
    _py: Python,
    m: &PyModule,
) -> PyResult<()> {
    m.add_class::<WordSegmenter>()?;

    Ok(())
}
