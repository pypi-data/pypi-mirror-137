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

use criterion::{black_box, criterion_group, criterion_main, Criterion};
extern crate rust_poly;
use ndarray::{
    s, Array, Array1, Array2, ArrayView, ArrayView1, ArrayView2, ArrayViewD, Dim, Dimension,
    IntoDimension, IxDynImpl, NdIndex, ScalarOperand, ShapeBuilder, SliceArg, SliceInfoElem,
};
use ndarray::{ArrayD, IxDyn};
use num_traits::cast::NumCast;
use num_traits::identities::{One, Zero};
use rust_poly::polynomial::{pow, Polynomial, PolynomialError};
use rust_poly::tree::Expression;
use std::ops::{Add, Div, Mul, Sub};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn make_poly_2d(f: f64, g: f64, h: f64, i: f64) -> Polynomial<f64> {
    let mut coefs = ArrayD::zeros(IxDyn(&[2, 2]));
    coefs[[0, 0]] = f;
    coefs[[0, 1]] = g;
    coefs[[1, 0]] = h;
    coefs[[1, 1]] = i;
    Polynomial::<f64>::new(coefs)
}

fn square_poly_2d(f: f64, g: f64, h: f64, i: f64) -> Result<Polynomial<f64>, PolynomialError> {
    let mut coefs = ArrayD::zeros(IxDyn(&[2, 2]));
    coefs[[0, 0]] = f;
    coefs[[0, 1]] = g;
    coefs[[1, 0]] = h;
    coefs[[1, 1]] = i;
    Polynomial::<f64>::new(coefs.clone()).mul(&Polynomial::<f64>::new(coefs.clone()))
}
fn mul_poly_2d(
    p1: &Polynomial<f64>,
    p2: &Polynomial<f64>,
) -> Result<Polynomial<f64>, PolynomialError> {
    p1.mul(&p2)
}
fn apply_poly_2d_manual(f: f64, g: f64, h: f64, i: f64, values: &Array2<f64>) -> Array1<f64> {
    let x: ArrayView1<_> = values.slice(s![.., 0]);
    let y: ArrayView1<_> = values.slice(s![.., 1]);
    f * Array1::ones([x.len()].into_dimension()) + g * &x + h * &y + i * &x * &y
}

fn criterion_benchmark(c: &mut Criterion) {
    // c.bench_function("make_poly_2d", |b| {
    //     b.iter(|| {
    //         make_poly_2d(
    //             black_box(1.0),
    //             black_box(2.0),
    //             black_box(3.0),
    //             black_box(4.0),
    //         )
    //     })
    // });
    let p1 = make_poly_2d(1.0, 2.0, 3.0, 4.0);
    let p2 = make_poly_2d(2.0, 3.0, 4.0, 5.0);
    // c.bench_function("square_poly_2d", |b| {
    //     b.iter(|| {
    //         square_poly_2d(
    //             black_box(1.0),
    //             black_box(2.0),
    //             black_box(3.0),
    //             black_box(4.0),
    //         )
    //     })
    // });
    // c.bench_function("mul_poly_2d", |b| {
    //     b.iter(|| mul_poly_2d(black_box(&p1), black_box(&p2)))
    // });
    let values = (0..2000000).map(|x| x as f64).collect::<Vec<_>>();
    let values = ArrayD::from_shape_vec(IxDyn(&[1000000, 2]), values).unwrap();
    c.bench_function("eval_poly_2d", |b| {
        b.iter(|| p1.eval(&values.view()).unwrap())
    });
    // For 1000000 values
    // Chunk sizes:
    // 10:      110.54 ms
    // 100:     21.4 ms
    // 1000:    13.68 ms
    // 2500:    11.29 ms
    // 5000:    11.08 ms
    // 10000:   11.774 ms
    // 25000:   12.60 ms
    // 50000:   16.586 ms
    // 100000:  21.08 ms

    // let values = (0..2000000).map(|x| x as f64).collect::<Vec<_>>();
    // c.bench_function("normal_pow", |b| {
    //     b.iter(|| black_box(&values).iter().map(|x| (*x).powi(5)).sum::<f64>())
    // });
    // c.bench_function("my_pow", |b| {
    //     b.iter(|| black_box(&values).iter().map(|x| pow(*x, 5)).sum::<f64>())
    // });
    // let values = Array2::from_shape_vec([1000000, 2].into_dimension(), values).unwrap();
    // c.bench_function("apply_poly_2d_manual", |b| {
    //     b.iter(|| {
    //         apply_poly_2d_manual(
    //             black_box(1.0),
    //             black_box(2.0),
    //             black_box(3.0),
    //             black_box(4.0),
    //             &values,
    //         )
    //     })
    // });

    // let values = (0..20000).map(|x| x as f64).collect::<Vec<f64>>();
    // c.bench_function("do_pows", |b| {
    //     b.iter(|| black_box(&values).iter().map(|x| x.powi(20)).sum::<f64>())
    // });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
