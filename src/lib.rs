use ahash::RandomState;
use flate2::Compression;
use flate2::write::GzEncoder;
use flate2::read::GzDecoder;
use once_cell::sync::Lazy;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use serde::{Serialize, Deserialize};
use smartstring::{SmartString, Compact};
use std::cmp;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, BufReader};

const MAX_WORD_LEN: usize = 24;

#[derive(Serialize, Deserialize, PartialEq, Debug, Default)]
struct WordSegmenter {
    unigrams: HashMap<String, f64, RandomState>,
    bigrams: HashMap<String, f64, RandomState>,
    total_words_frequency: f64,
}

static WORD_SEGMENTER: Lazy<WordSegmenter> = Lazy::new(
    || {
        let word_segmenter_file = File::open("/home/wavenator/work/pywordsegment/pywordsegment/pywordsegment/word_segmenter.bincode").unwrap();
        let word_segmenter_file = BufReader::new(word_segmenter_file);
        let decoder = GzDecoder::new(word_segmenter_file);

        bincode::deserialize_from(decoder).unwrap()
    }
);


#[pymodule]
fn pywordsegment(
    _py: Python,
    m: &PyModule,
) -> PyResult<()> {
    #[pyfn(m)]
    fn create_dictionary_file(
        unigrams: HashMap<String, f64, RandomState>,
        bigrams: HashMap<String, f64, RandomState>,
        total_words_frequency: f64,
    ) -> PyResult<()> {
        let word_segmenter = WordSegmenter {
            unigrams,
            bigrams,
            total_words_frequency,
        };
        let word_segmenter_file = File::create("word_segmenter.bincode")?;
        let word_segmenter_file = BufWriter::new(word_segmenter_file);

        let encoder = GzEncoder::new(word_segmenter_file, Compression::default());

        bincode::serialize_into(encoder, &word_segmenter)
            .map_err(|err| PyRuntimeError::new_err(format!("Could not serialize: {:?}", err)))
    }

    #[pyfn(m)]
    fn segment(
        py: Python,
        text: String,
    ) -> PyResult<Py<PyAny>> {
        let clean_text = text
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );

        let n = clean_text.len();
        let clean_text_len_triangular_number = (n * (n + 1) * (n + 2)) / 6;
        let mut memo = HashMap::with_capacity(clean_text_len_triangular_number);

        let (_score, words) = search(&mut memo, &clean_text, "<s>");

        Ok(words.into_py(py))
    }

    #[pyfn(m)]
    fn exist_as_segment(
        substring: String,
        text: String,
    ) -> PyResult<bool> {
        let clean_text = text
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );

        let clean_substring = substring
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );

        let n = cmp::max(clean_text.len(), clean_substring.len());
        let clean_text_len_triangular_number = (n * (n + 1) * (n + 2)) / 6;
        let mut memo = HashMap::with_capacity(clean_text_len_triangular_number);

        let (_score, segmented_text) = search(&mut memo, &clean_text, "<s>");
        memo.clear();
        let (_score, segmented_substring) = search(&mut memo, &clean_substring, "<s>");

        let segmented_substring_pattern = format!("-{}-", segmented_substring.join("-"));
        let segmented_text_pattern = format!("-{}-", segmented_text.join("-"));

        Ok(segmented_text_pattern.contains(&segmented_substring_pattern))
    }

    fn score(
        word: &str,
        previous: &str,
    ) -> f64 {
        if WORD_SEGMENTER.unigrams.contains_key(previous) {
            let mut bigram = SmartString::<Compact>::new();
            bigram.push_str(previous);
            bigram.push_str(" ");
            bigram.push_str(word);
            if let Some(bigram_frequency) = WORD_SEGMENTER.bigrams.get(bigram.as_str()) {
                return bigram_frequency / WORD_SEGMENTER.unigrams.get(previous).unwrap();
            }
        }
        match WORD_SEGMENTER.unigrams.get(word) {
            Some(frequency) => frequency / WORD_SEGMENTER.total_words_frequency,
            None => 10.0 / (WORD_SEGMENTER.total_words_frequency * 10_f64.powi(word.len() as i32)),
        }
    }

    fn search<'a>(
        memo: &mut HashMap<(&'a str, &'a str), (f64, Vec<&'a str>)>,
        text: &'a str,
        previous: &str,
    ) -> (f64, Vec<&'a str>) {
        let mut best_candidate = (-100000.0, Vec::new());
        for pos in 1..cmp::min(text.len(), MAX_WORD_LEN) + 1 {
            let prefix = &text[..pos];
            let suffix = &text[pos..];
            let prefix_score = score(prefix, previous).log10();

            if let Some((suffix_score, suffix_words)) = memo.get(&(suffix, prefix)) {
                if best_candidate.0 < prefix_score + suffix_score {
                    best_candidate.0 = prefix_score + suffix_score;
                    best_candidate.1.clear();
                    best_candidate.1.push(prefix);
                    best_candidate.1.extend(suffix_words);
                }
            } else if suffix.is_empty() {
                if best_candidate.0 < prefix_score {
                    best_candidate.0 = prefix_score;
                    best_candidate.1.clear();
                    best_candidate.1.push(prefix);
                }
                memo.insert((suffix, prefix), (0.0, Vec::new()));
            } else {
                let (suffix_score, suffix_words) = search(memo, suffix, prefix);
                if best_candidate.0 < prefix_score + suffix_score {
                    best_candidate.0 = prefix_score + suffix_score;
                    best_candidate.1.clear();
                    best_candidate.1.push(prefix);
                    best_candidate.1.extend(&suffix_words);
                }
                memo.insert((suffix, prefix), (suffix_score, suffix_words));
            }
        }

        best_candidate
    }

    Ok(())
}
