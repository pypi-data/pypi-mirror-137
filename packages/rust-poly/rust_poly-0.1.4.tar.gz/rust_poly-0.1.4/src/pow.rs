use ndarray::ArrayD;
use num_complex::Complex;

/// Convenience trait for consolidating Pow
pub trait Pow<RHS> {
    type Output;
    fn pow(self, rhs: RHS) -> Self::Output;
}

impl Pow<usize> for i64 {
    type Output = Self;
    fn pow(self, rhs: usize) -> Self::Output {
        num_traits::pow::Pow::pow(self, rhs)
    }
}

impl Pow<usize> for f64 {
    type Output = Self;
    fn pow(self, rhs: usize) -> Self::Output {
        self.powi(rhs as i32)
    }
}

impl Pow<usize> for Complex<f64> {
    type Output = Self;
    fn pow(self, rhs: usize) -> Self::Output {
        self.powi(rhs as i32)
    }
}

impl<T> Pow<usize> for ArrayD<T>
where
    T: Pow<usize, Output = T> + Clone,
{
    type Output = Self;
    fn pow(self, rhs: usize) -> Self::Output {
        self.mapv(|x| x.pow(rhs))
    }
}
