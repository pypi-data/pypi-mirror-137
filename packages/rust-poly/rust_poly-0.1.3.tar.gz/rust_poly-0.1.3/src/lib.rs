// The MIT License (MIT)
//
//     Copyright (c) 2022 Jason Ross
//
//     Permission is hereby granted, free of charge, to any person obtaining a copy
//     of this software and associated documentation files (the "Software"), to
//     deal in the Software without restriction, including without limitation the
//     rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
//     sell copies of the Software, and to permit persons to whom the Software is
//     furnished to do so, subject to the following conditions:
//
//     The above copyright notice and this permission notice shall be included in
//     all copies or substantial portions of the Software.
//
//     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
//     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
//     IN THE SOFTWARE.

use numpy::npyffi::array::PY_ARRAY_API;
use numpy::npyffi::types::NPY_TYPES;
use numpy::{
    IntoPyArray, PyArray1, PyReadonlyArray1, PyReadonlyArrayDyn,
};
use polynomial::PolynomialError;
use pyo3::conversion::FromPyPointer;
use pyo3::exceptions::PyValueError;
use pyo3::types::PyType;
use pyo3::{prelude::*, AsPyPointer};

use num_complex::Complex;
use pyo3::{PyNumberProtocol, PyObjectProtocol};
use tree::Expression;
pub mod polynomial;
pub mod pow;
pub mod tree;

/// An abstract expression tree with concrete terms. Lazily evaluates arithmetic
/// operations.
#[derive(Clone)]
#[pyclass]
#[pyo3(text_signature = "(vals)")]
struct ExpressionTree {
    expression: ExpressionType,
}

#[derive(Clone)]
enum ExpressionType {
    Float(Expression<f64>),
    Complex(Expression<Complex<f64>>),
    Int(Expression<i64>),
}

impl ExpressionType {
    fn shape(&self) -> Vec<usize> {
        use ExpressionType::*;
        match self {
            Float(e) => e.shape(),
            Complex(e) => e.shape(),
            Int(e) => e.shape(),
        }
    }
    fn dimension(&self) -> usize {
        use ExpressionType::*;
        match self {
            Float(e) => e.dimension(),
            Complex(e) => e.dimension(),
            Int(e) => e.dimension(),
        }
    }
    fn expand(&self) -> PyResult<Self> {
        use ExpressionType::*;
        match self {
            Float(e) => Ok(Float(e.expand()?.to_expression()?)),
            Complex(e) => Ok(Complex(e.expand()?.to_expression()?)),
            Int(e) => Ok(Int(e.expand()?.to_expression()?)),
        }
    }
    fn deriv_integ(&self, indices: &[isize]) -> PyResult<Self> {
        use ExpressionType::*;
        match self {
            Float(e) => Ok(Float(e.deriv_integ(indices)?)),
            Complex(e) => Ok(Complex(e.deriv_integ(indices)?)),
            Int(e) => Ok(Int(e.deriv_integ(indices)?)),
        }
    }
    fn drop_params(&self, indices: &[usize]) -> PyResult<Self> {
        use ExpressionType::*;
        match self {
            Float(e) => Ok(Float(e.drop_params(indices)?)),
            Complex(e) => Ok(Complex(e.drop_params(indices)?)),
            Int(e) => Ok(Int(e.drop_params(indices)?)),
        }
    }
    fn add(&self, right: &Self) -> PyResult<Self> {
        use ExpressionType::*;
        match (self, right) {
            (Float(f), Complex(c)) | (Complex(c), Float(f)) => Ok(Complex(c.add(&f.astype()?)?)),
            (Float(f), Int(i)) | (Int(i), Float(f)) => Ok(Float(f.add(&i.astype()?)?)),
            (Complex(c), Int(i)) | (Int(i), Complex(c)) => Ok(Complex(c.add(&i.astype()?)?)),
            (Float(l), Float(r)) => Ok(Float(l.add(r)?)),
            (Complex(l), Complex(r)) => Ok(Complex(l.add(r)?)),
            (Int(l), Int(r)) => Ok(Int(l.add(r)?)),
        }
    }
    fn sub(&self, right: &Self) -> PyResult<Self> {
        use ExpressionType::*;
        match (self, right) {
            (Float(f), Complex(c)) | (Complex(c), Float(f)) => Ok(Complex(c.sub(&f.astype()?)?)),
            (Float(f), Int(i)) | (Int(i), Float(f)) => Ok(Float(f.sub(&i.astype()?)?)),
            (Complex(c), Int(i)) | (Int(i), Complex(c)) => Ok(Complex(c.sub(&i.astype()?)?)),
            (Float(l), Float(r)) => Ok(Float(l.sub(r)?)),
            (Complex(l), Complex(r)) => Ok(Complex(l.sub(r)?)),
            (Int(l), Int(r)) => Ok(Int(l.sub(r)?)),
        }
    }
    fn mul(&self, right: &Self) -> PyResult<Self> {
        use ExpressionType::*;
        match (self, right) {
            (Float(f), Complex(c)) | (Complex(c), Float(f)) => Ok(Complex(c.mul(&f.astype()?)?)),
            (Float(f), Int(i)) | (Int(i), Float(f)) => Ok(Float(f.mul(&i.astype()?)?)),
            (Complex(c), Int(i)) | (Int(i), Complex(c)) => Ok(Complex(c.mul(&i.astype()?)?)),
            (Float(l), Float(r)) => Ok(Float(l.mul(r)?)),
            (Complex(l), Complex(r)) => Ok(Complex(l.mul(r)?)),
            (Int(l), Int(r)) => Ok(Int(l.mul(r)?)),
        }
    }
    fn div(&self, right: &Self) -> PyResult<Self> {
        use ExpressionType::*;
        match (self, right) {
            (Float(f), Complex(c)) | (Complex(c), Float(f)) => Ok(Complex(c.div(&f.astype()?)?)),
            (Float(f), Int(i)) | (Int(i), Float(f)) => Ok(Float(f.div(&i.astype()?)?)),
            (Complex(c), Int(i)) | (Int(i), Complex(c)) => Ok(Complex(c.div(&i.astype()?)?)),
            (Float(l), Float(r)) => Ok(Float(l.div(r)?)),
            (Complex(l), Complex(r)) => Ok(Complex(l.div(r)?)),
            (Int(l), Int(r)) => Ok(Int(l.div(r)?)),
        }
    }
}

impl std::fmt::Display for ExpressionType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        use ExpressionType::*;
        match self {
            Float(e) => write!(f, "{}, dtype = f64", e),
            Complex(e) => write!(f, "{}, dtype = c64", e),
            Int(e) => write!(f, "{}, dtype = i64", e),
        }
    }
}

/// Converts a python object to a numpy array using the numpy API.
unsafe fn array_from_any<'py>(
    object: PyObject,
    py: &'py Python<'py>,
    descr: NPY_TYPES,
) -> &'py PyAny {
    use numpy::npyffi::objects::PyArray_Descr;
    let mintype: *mut PyArray_Descr = PY_ARRAY_API.PyArray_DescrFromType((descr as u32) as i32);
    let ob_ptr: *mut pyo3::ffi::PyObject = object.as_ptr();
    let desc = PY_ARRAY_API.PyArray_DescrFromObject(ob_ptr, mintype);
    let context: *mut pyo3::ffi::PyObject = std::ptr::null_mut();
    let ar = PY_ARRAY_API.PyArray_FromAny(ob_ptr, desc, 0, 32, 0, context);
    PyAny::from_borrowed_ptr(*py, ar)
}

#[pymethods]
impl ExpressionTree {
    #[new]
    fn new<'py>(py: Python<'py>, vals: &PyAny) -> PyResult<Self> {
        let vals = unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_LONGLONG) };
        if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<i64>>() {
            let p = crate::polynomial::Polynomial::<i64>::new(vals.as_array().to_owned());
            return Ok(ExpressionTree {
                expression: ExpressionType::Int(Expression::polynomial(&p)),
            });
        }
        let vals = unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_DOUBLE) };
        if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<f64>>() {
            let p = crate::polynomial::Polynomial::<f64>::new(vals.as_array().to_owned());
            return Ok(ExpressionTree {
                expression: ExpressionType::Float(Expression::polynomial(&p)),
            });
        }
        let vals = unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_CDOUBLE) };
        if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<Complex<f64>>>() {
            let p = crate::polynomial::Polynomial::<Complex<f64>>::new(vals.as_array().to_owned());
            return Ok(ExpressionTree {
                expression: ExpressionType::Complex(Expression::polynomial(&p)),
            });
        }
        Err(PyValueError::new_err("Unsupported data type returned"))
    }
    /// Evaluates the expression on an array of values.
    ///
    /// Parameters
    /// ==========
    ///
    /// vals : array_like
    ///     Shape (a, b, ..., z, n) where n matches the dimension of the expression tree
    ///
    /// Returns
    /// array_like
    ///     Shape (a, b, ..., z)
    fn __call__<'py>(&self, py: Python<'py>, vals: &PyAny) -> PyResult<PyObject> {
        use ExpressionType::*;
        match &self.expression {
            Float(e) => {
                let vals =
                    unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_DOUBLE) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<f64>>() {
                    return Ok(e.eval(&vals.as_array())?.into_pyarray(py).to_object(py));
                }
            }
            Complex(e) => {
                let vals =
                    unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_CDOUBLE) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<num_complex::Complex<f64>>>() {
                    return Ok(e.eval(&vals.as_array())?.into_pyarray(py).to_object(py));
                }
            }
            Int(e) => {
                let vals =
                    unsafe { array_from_any(vals.to_object(py), &py, NPY_TYPES::NPY_LONGLONG) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<i64>>() {
                    return Ok(e.eval(&vals.as_array())?.into_pyarray(py).to_object(py));
                }
            }
        }
        Err(PyValueError::new_err(
            "Unsupported data type for evaluation",
        ))
    }

    /// The maximum degree of any term in the expression tree
    #[getter]
    fn shape<'py>(&self, py: Python<'py>) -> &'py PyArray1<usize> {
        self.expression.shape().into_pyarray(py)
    }
    /// The number of free parameters in the expression tree
    #[getter]
    fn dimension(&self) -> usize {
        self.expression.dimension()
    }
    /// Recursively evaluate the syntax tree to yield either a single polynomial
    /// or a rational with a polynomial numerator and denominator.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[pyo3(text_signature = "()")]
    fn expand(&self) -> PyResult<Self> {
        Ok(ExpressionTree {
            expression: self.expression.expand()?,
        })
    }
    /// Evaluate the expression tree on a subset of provided terms and return a
    /// new expression tree.
    ///
    /// Parameters
    /// ==========
    /// indicies : array_like
    ///     (n,) shaped array of integers. This argument specifies which terms in the
    ///     expression are to be evaluated.
    /// values : array_like
    ///     (n,) shaped array of floats. This argument specifies the values to use in
    ///     the expression.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[pyo3(text_signature = "(indices, values)")]
    fn partial<'py>(&self, py: Python<'py>, indices: &PyAny, values: &PyAny) -> PyResult<Self> {
        let indices =
            unsafe { array_from_any(indices.to_object(py), &py, NPY_TYPES::NPY_LONGLONG) }
                .extract::<PyReadonlyArray1<i64>>()
                .map_err(|_| PolynomialError::Other("Index format not understood".to_string()))?;

        // Annoying way of getting an array of usize from an array of isize or error.
        use std::mem::MaybeUninit;
        use ndarray::Array1;
        use num_traits::NumCast;
        let mut output = Array1::uninit(indices.as_array().dim());
        for (index, value) in output.indexed_iter_mut() {
            let toval: usize = NumCast::from(*indices.get(index).ok_or_else(|| {
                PolynomialError::Other("Some kind of crazy lookup error".to_string())
            })?)
            .ok_or_else(|| PolynomialError::Other("Could not convert data type".to_string()))?;
            *value = MaybeUninit::new(toval);
        }
        let indices = unsafe { output.assume_init() };

        // This could probably be replaced with a macro
        use ExpressionType::*;
        match &self.expression {
            Float(e) => {
                let vals =
                    unsafe { array_from_any(values.to_object(py), &py, NPY_TYPES::NPY_DOUBLE) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.partial(
                            indices.as_slice().ok_or_else(|| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                            vals.as_slice().map_err(|_| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                        )?),
                    });
                };
            }
            Complex(e) => {
                let vals =
                    unsafe { array_from_any(values.to_object(py), &py, NPY_TYPES::NPY_CDOUBLE) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<num_complex::Complex<f64>>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.partial(
                            indices.as_slice().ok_or_else(|| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                            vals.as_slice().map_err(|_| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                        )?),
                    });
                };
            }
            Int(e) => {
                let vals =
                    unsafe { array_from_any(values.to_object(py), &py, NPY_TYPES::NPY_LONGLONG) };
                if let Ok(vals) = vals.extract::<PyReadonlyArrayDyn<i64>>() {
                    return Ok(ExpressionTree {
                        expression: Int(e.partial(
                            indices.as_slice().ok_or_else(|| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                            vals.as_slice().map_err(|_| {
                                PolynomialError::Other(
                                    "Could not convert indices to slice".to_string(),
                                )
                            })?,
                        )?),
                    });
                }
            }
        };
        Err(PyValueError::new_err(
            "Unsupported data type for evaluation",
        ))
    }
    /// Takes the derivative of the expression with respect to multiple
    /// parameters. Zero is a no-op. Negative numbers integrate.
    ///
    /// Parameters
    /// ==========
    /// indices: array_like of int
    ///     shape (n,) where n is the dimension of the expression.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[pyo3(text_signature = "(indices)")]
    fn deriv(&self, indices: PyReadonlyArray1<i64>) -> PyResult<Self> {
        let indices = indices.as_array();
        let indices = {
            let mut indices_ = vec![];
            for index in indices {
                indices_.push(*index as isize);
            }
            indices_
        };
        Ok(ExpressionTree {
            expression: self.expression.deriv_integ(&indices)?,
        })
    }
    /// Takes the antiderivative of the expression with respect to multiple
    /// parameters. Zero is a no-op. Negative numbers differentiate.
    ///
    /// Parameters
    /// ==========
    /// indices: array_like of int
    ///     shape (n,) where n is the dimension of the expression.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[pyo3(text_signature = "(indices)")]
    fn integ(&self, indices: PyReadonlyArray1<i64>) -> PyResult<Self> {
        let indices = indices.as_array();
        let indices = {
            let mut indices_ = vec![];
            for index in indices {
                indices_.push(-*index as isize);
            }
            indices_
        };
        Ok(ExpressionTree {
            expression: self.expression.deriv_integ(&indices)?,
        })
    }
    /// Try to drop parameters and reduce the dimensionality.
    ///
    /// Parameters
    /// ==========
    /// indices: array_like of int
    ///     shape (m,), specifies degrees of freedom to drop.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    ///
    /// Raises
    /// ======
    /// ValueError
    ///     If non-empty or invalid degrees of freedom are specified.
    #[pyo3(text_signature = "(indices)")]
    fn drop_params(&self, indices: PyReadonlyArray1<i64>) -> PyResult<Self> {
        let indices = indices.as_array();
        let indices = {
            let mut indices_ = vec![];
            for index in indices {
                if *index < 0 {
                    return Err(
                        PolynomialError::Other("Negative indices not allowed".to_string()).into(),
                    );
                }
                indices_.push(*index as usize);
            }
            indices_
        };
        Ok(ExpressionTree {
            expression: self.expression.drop_params(&indices)?,
        })
    }
    /// Automatically drop empty degrees of freedom
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[pyo3(text_signature = "()")]
    fn squeeze(&self) -> PyResult<Self> {
        let to_drop = self
            .expression
            .shape()
            .iter()
            .enumerate()
            .filter_map(|(i, v)| if *v == 1 { Some(i) } else { None })
            .collect::<Vec<_>>();
        Ok(ExpressionTree {
            expression: self.expression.drop_params(to_drop.as_slice())?,
        })
    }
    /// Try to evaluate the expression and return a constant
    ///
    /// Raises
    /// ======
    ///
    /// ValueError
    ///     If some degrees of freedom still exist
    #[pyo3(text_signature = "()")]
    fn to_constant<'py>(&'py self, py: Python<'py>) -> PyResult<PyObject> {
        use ExpressionType::*;
        match &self.expression {
            Float(e) => {
                let v = e.to_constant()?;
                Ok(v.into_py(py))
            }
            Complex(e) => {
                let v = e.to_constant()?;
                Ok(v.into_py(py))
            }
            Int(e) => {
                let v = e.to_constant()?;
                Ok(v.into_py(py))
            }
        }
        // Ok(self.expression.to_constant()?)
    }
    // TODO Some kind of "Kind"

    /// Construct a polynomial of desired dimension equal to the constant 1.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[classmethod]
    #[pyo3(text_signature = "()")]
    fn zero(_cls: &PyType, dimension: i64) -> PyResult<Self> {
        if dimension < 0 {
            return Err(PolynomialError::Other("Negative dimension is invalid".to_string()).into());
        }
        let dimension = dimension as usize;
        Ok(ExpressionTree {
            expression: ExpressionType::Float(Expression::zero(dimension)),
        })
    }
    /// Construct a polynomial of desired dimension equal to the constant 0.
    ///
    /// Returns
    /// =======
    /// FloatExpression
    #[classmethod]
    #[pyo3(text_signature = "()")]
    fn one(_cls: &PyType, dimension: i64) -> PyResult<Self> {
        if dimension < 0 {
            return Err(PolynomialError::Other("Negative dimension is invalid".to_string()).into());
        }
        let dimension = dimension as usize;
        Ok(ExpressionTree {
            expression: ExpressionType::Float(Expression::one(dimension)),
        })
    }
}

#[pyproto]
impl PyObjectProtocol for ExpressionTree {
    fn __str__(&'p self) -> PyResult<String> {
        Ok(format!("{}", self.expression))
    }
}

#[pyproto]
impl PyNumberProtocol for ExpressionTree {
    fn __add__(lhs: Self, rhs: Self) -> PyResult<Self> {
        Ok(ExpressionTree {
            expression: lhs.expression.add(&rhs.expression)?,
        })
    }
    fn __sub__(lhs: Self, rhs: Self) -> PyResult<Self> {
        Ok(ExpressionTree {
            expression: lhs.expression.sub(&rhs.expression)?,
        })
    }
    fn __truediv__(lhs: Self, rhs: &'p PyAny) -> PyResult<Self> {
        if let Ok(ExpressionTree { expression: other }) = rhs.extract() {
            return Ok(ExpressionTree {
                expression: lhs.expression.div(&other)?,
            });
        };

        use ExpressionType::*;
        match lhs.expression {
            Float(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(1.0 / v as f64)?)
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(1.0 / v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(1.0 / v)?)
                    });
                }
            }
            Complex(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(1.0 / v as f64)?),
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(1.0 / v)?),
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(1.0 / v)?)
                    });
                }
            }
            Int(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(1.0 / v as f64)?)
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(1.0 / v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(1.0 / v)?)
                    });
                }
            }
        };
        Err(PyValueError::new_err("Invalid type provided for division"))
    }
    fn __mul__(lhs: Self, rhs: &'p PyAny) -> PyResult<Self> {
        if let Ok(ExpressionTree { expression: other }) = rhs.extract() {
            return Ok(ExpressionTree {
                expression: lhs.expression.mul(&other)?,
            });
        };
        use ExpressionType::*;
        match lhs.expression {
            Float(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(v)?)
                    });
                }
            }
            Complex(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(v)?),
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(v)?),
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(v)?)
                    });
                }
            }
            Int(e) => {
                if let Ok(v) = rhs.extract::<i64>() {
                    return Ok(ExpressionTree {
                        expression: Int(e.scale(v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<f64>() {
                    return Ok(ExpressionTree {
                        expression: Float(e.scale(v)?)
                    });
                }
                if let Ok(v) = rhs.extract::<num_complex::Complex<f64>>() {
                    return Ok(ExpressionTree {
                        expression: Complex(e.scale(v)?)
                    });
                }
            }
        };
        Err(PyValueError::new_err(
            "Invalid type provided for multiplication",
        ))
    }

    fn __rmul__(&self, other: &'p PyAny) -> PyResult<Self> {
        Self::__mul__(self.clone(), other)
    }
}

/// Provides the ExpressionTree class
#[pymodule]
#[pyo3(name = "rust_poly")]
fn polynomial(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExpressionTree>()?;
    Ok(())
}
