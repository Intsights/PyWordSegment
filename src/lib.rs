use ahash::RandomState;
use pyo3::prelude::*;
use std::collections::HashMap;

const MAX_WORD_LEN: usize = 24;

#[pyclass]
struct WordSegmenter {
    unigrams: HashMap<String, f64, RandomState>,
    bigrams: HashMap<String, HashMap<String, f64, RandomState>, RandomState>,
    unknown_unigrams: [f64; MAX_WORD_LEN + 1],
}

#[pymethods]
impl WordSegmenter {
    #[new]
    fn new(
        unigrams_serialized: &[u8],
        bigrams_serialized: &[u8],
    ) -> Self {
        let unigrams: HashMap<String, f64, RandomState> = rmp_serde::from_slice(unigrams_serialized).unwrap();
        let bigrams = rmp_serde::from_slice(bigrams_serialized).unwrap();

        let total_unigrams_frequency = unigrams.get("unigrams_total_count").unwrap();
        let mut unknown_unigrams = [0.0; MAX_WORD_LEN + 1];
        for (word_len, value) in unknown_unigrams.iter_mut().enumerate() {
            *value = (10.0 / (total_unigrams_frequency * 10_f64.powi(word_len as i32))).log10();
        }

        WordSegmenter {
            unigrams,
            bigrams,
            unknown_unigrams,
        }
    }

    fn segment(
        &self,
        py: Python,
        text: String,
    ) -> PyResult<Py<PyAny>> {
        let clean_text = text
            .to_ascii_lowercase()
            .replace(
                |c: char| !c.is_ascii_alphanumeric(),
                ""
            );

        let words = self.search(&clean_text);

        Ok(words.into_py(py))
    }

    fn exist_as_segment(
        &self,
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

        let segmented_text = self.search(&clean_text);
        let segmented_substring = self.search(&clean_substring);

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
        if !previous.is_empty() {
            if let Some(first_bigram_layer) = self.bigrams.get(previous) {
                if let Some(bigram_frequency) = first_bigram_layer.get(word) {
                    return *bigram_frequency;
                }
            }
        }

        match self.unigrams.get(word) {
            Some(frequency) => *frequency,
            None => self.unknown_unigrams[word.len()],
        }
    }

    fn search<'a>(
        &self,
        text: &'a str,
    ) -> Vec<&'a str> {
        let mut result = Vec::with_capacity(text.len());
        let mut candidates = Vec::with_capacity(text.len());

        if text.is_empty() {
            return result;
        }

        for end in 1..=text.len() {
            let start = end.saturating_sub(MAX_WORD_LEN);
            for split in start..end {
                let (prev, prev_score) = match split {
                    0 => ("", 0.0),
                    _ => {
                        let (prefix_len, prefix_score) = candidates[split - 1];
                        let word = &text[split - prefix_len as usize..split];
                        (word, prefix_score)
                    }
                };

                let word = &text[split..end];
                let score = self.score(word, prev) + prev_score;
                match candidates.get_mut(end - 1) {
                    Some((cur_len, cur_score)) if *cur_score < score => {
                        *cur_len = end - split;
                        *cur_score = score;
                    }
                    None => candidates.push((end - split, score)),
                    _ => {},
                }
            }
        }

        let mut end = text.len();
        let (mut best_len, mut _best_score) = candidates[end - 1];
        loop {
            let word = &text[end - best_len..end];
            result.insert(0, word);

            end -= best_len;
            if end == 0 {
                break;
            }

            best_len = candidates[end - 1].0;
        }

        result
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
