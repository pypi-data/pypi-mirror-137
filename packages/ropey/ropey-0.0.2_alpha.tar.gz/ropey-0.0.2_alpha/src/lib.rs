use pyo3::exceptions::PyNotImplementedError;
use pyo3::prelude::*;
use pyo3::types::PySlice;
use ropey::{Rope, RopeBuilder};
use std::fs::File;
use std::io;
use std::io::{BufReader, BufWriter};

#[pyclass(name = "Rope")]
#[derive(Clone, Debug)]
struct PyRope {
    rope: Rope,
}

#[pymethods]
impl PyRope {
    /// Create an empty Rope.
    #[new]
    fn new() -> PyRope {
        PyRope { rope: Rope::new() }
    }

    fn __str__(&self) -> String {
        format!("{}", self.rope)
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.rope)
    }

    /// Content of the Rope as a string.
    ///
    /// :return: string
    #[getter]
    fn text(&self) -> String {
        self.__str__()
    }

    /// Creates a Rope from a string slice.
    ///
    /// :param s: string
    /// :return: Rope
    #[pyo3(text_signature = "(s, /)")]
    #[staticmethod]
    fn from_str(s: &str) -> PyRope {
        PyRope {
            rope: Rope::from_str(s),
        }
    }

    /// Creates a Rope from the output of a reader.
    ///
    /// :param reader: reader
    /// :return: Rope
    #[pyo3(text_signature = "(reader, /)")]
    #[staticmethod]
    fn from_reader(_reader: PyObject) -> PyResult<()> {
        Err(PyNotImplementedError::new_err(
            "Cannot currently convert Python reader to Rust reader",
        ))
    }

    /// Creates a Rope from a file.
    ///
    /// :param f: filename
    /// :return: Rope
    #[pyo3(text_signature = "(f, /)")]
    #[staticmethod]
    fn from_file(f: &str) -> io::Result<Self> {
        Ok(PyRope {
            rope: Rope::from_reader(BufReader::new(File::open(f)?))?,
        })
    }

    /// Writes to content of the Rope to a writer.
    ///
    /// :param writer: writer
    #[pyo3(text_signature = "(writer, /)")]
    fn write_to(&self, _writer: PyObject) -> PyResult<()> {
        Err(PyNotImplementedError::new_err(
            "Cannot currently convert Python writer to Rust writer",
        ))
    }

    /// Writes to content of the Rope to a file.
    ///
    /// :param f: filename
    #[pyo3(text_signature = "(f, /)")]
    fn write_to_file(&self, f: &str) -> io::Result<()> {
        self.rope.write_to(BufWriter::new(File::create(f)?))?;
        Ok(())
    }

    /// Total number of bytes in the Rope.
    ///
    /// :return: number of bytes
    fn len_bytes(&self) -> usize {
        self.rope.len_bytes()
    }

    /// Total number of chars in the Rope.
    ///
    /// :return: number of chars
    fn len_chars(&self) -> usize {
        self.rope.len_chars()
    }

    /// Total number of lines in the Rope.
    ///
    /// :return: number of lines
    fn len_lines(&self) -> usize {
        self.rope.len_lines()
    }

    /// Total number of utf16 code units that would be in Rope if it were encoded as utf16.
    ///
    /// :return: number of utf16 code units
    fn len_utf16_cu(&self) -> usize {
        self.rope.len_utf16_cu()
    }

    /// Total size of the Rope’s text buffer space, in bytes.
    ///
    /// :return: capacity
    fn capacity(&self) -> usize {
        self.rope.capacity()
    }

    /// Shrinks the Rope’s capacity to the minimum possible.
    fn shrink_to_fit(&mut self) {
        self.rope.shrink_to_fit()
    }

    /// Inserts text at char index char_idx.
    ///
    /// :param char_idx: char index
    /// :param text: text
    #[pyo3(text_signature = "(char_idx, text, /)")]
    fn insert(&mut self, char_idx: usize, text: &str) {
        self.rope.insert(char_idx, text)
    }

    /// Inserts a single char ch at char index char_idx.
    ///
    /// :param char_idx: char index
    /// :param ch: char
    #[pyo3(text_signature = "(char_idx, ch, /)")]
    fn insert_char(&mut self, char_idx: usize, ch: char) {
        self.rope.insert_char(char_idx, ch)
    }

    #[inline]
    fn remove_range(&mut self, char_start: usize, char_end: usize) {
        self.rope.remove(char_start..char_end)
    }

    #[inline]
    fn remove_range_from(&mut self, char_start: usize) {
        self.rope.remove(char_start..)
    }

    #[inline]
    fn remove_range_to(&mut self, char_end: usize) {
        self.rope.remove(..char_end)
    }

    #[inline]
    fn remove_range_full(&mut self) {
        self.rope.remove(..)
    }

    /// Removes the text in the given char index range.
    ///
    /// In the Python slice:
    ///     - start: int or None, None sets start to 0
    ///     - stop: int or None, None sets stop to self.len_chars()
    ///     - step: unused
    ///
    /// :param char_range: range
    #[pyo3(text_signature = "(char_range, /)")]
    fn remove(&mut self, char_range: &PySlice) -> PyResult<()> {
        let start = {
            let s = char_range.getattr("start")?;
            if s.is_none() {
                None
            } else {
                Some(s.extract()?)
            }
        };
        let stop = {
            let s = char_range.getattr("stop")?;
            if s.is_none() {
                None
            } else {
                Some(s.extract()?)
            }
        };

        if let Some(start) = start {
            if let Some(stop) = stop {
                self.remove_range(start, stop);
            } else {
                self.remove_range_from(start);
            }
        } else if let Some(stop) = stop {
            self.remove_range_to(stop);
        } else {
            self.remove_range_full();
        }
        Ok(())
    }

    /// Splits the Rope at char_idx, returning the right part of the split.
    ///
    /// :param char_idx: char index
    #[pyo3(text_signature = "(char_idx, /)")]
    fn split_off(&mut self, char_idx: usize) -> Self {
        PyRope {
            rope: self.rope.split_off(char_idx),
        }
    }

    /// Appends a Rope to the end of this one, consuming the other Rope.
    ///
    /// :Note:
    /// In Python, the other Rope is cloned due to PyO3 restrictions.
    ///
    /// :param other: other Rope
    #[pyo3(text_signature = "(other, /)")]
    fn append(&mut self, other: Self) {
        self.rope.append(other.rope)
    }
}

#[pyclass(name = "RopeBuilder")]
#[derive(Clone, Debug)]
struct PyRopeBuilder {
    rope_builder: RopeBuilder,
}

#[pymethods]
impl PyRopeBuilder {
    /// Creates a new RopeBuilder, ready for input.
    #[new]
    fn new() -> PyRopeBuilder {
        PyRopeBuilder {
            rope_builder: RopeBuilder::new(),
        }
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.rope_builder)
    }

    /// Appends chunk to the end of the in-progress Rope.
    ///
    /// :param chunk: chunk
    #[pyo3(text_signature = "(chunk, /)")]
    fn append(&mut self, chunk: &str) {
        self.rope_builder.append(chunk)
    }

    /// Finishes the build, and returns the Rope.
    ///
    /// :return: Rope
    fn finish(&mut self) -> PyRope {
        PyRope {
            rope: self.rope_builder.clone().finish(),
        }
    }
}

/// Ropey module exposed to Python users.
#[pymodule]
fn ropey(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyRope>()?;
    m.add_class::<PyRopeBuilder>()?;
    Ok(())
}
