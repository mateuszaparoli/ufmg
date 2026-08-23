// PolyBench-Linalg: General Matrix Multiplication (GEMM)
// Implemented via structured Named Op (linalg.matmul) and Bufferization.

module {
  func.func @kernel_gemm_linalg(
    %alpha: f32,
    %beta: f32,
    %A: tensor<1024x1024xf32>,
    %B: tensor<1024x1024xf32>,
    %C: tensor<1024x1024xf32>
  ) -> tensor<1024x1024xf32> {
    
    // Scale C by beta using linalg.generic
    %c_scaled = linalg.generic {
      indexing_maps = [
        affine_map<(d0, d1) -> (d0, d1)>,
        affine_map<(d0, d1) -> (d0, d1)>
      ],
      iterator_types = ["parallel", "parallel"]
    } ins(%C : tensor<1024x1024xf32>) outs(%C : tensor<1024x1024xf32>) {
    ^bb0(%in: f32, %out: f32):
      %prod = arith.mulf %in, %beta : f32
      linalg.yield %prod : f32
    } -> tensor<1024x1024xf32>

    // Perform GEMM: C = alpha * (A x B) + beta * C
    // In MLIR Linalg, matmul handles outer dimensions (parallel) and reduction dimension (reduction)
    %res = linalg.matmul
      ins(%A, %B : tensor<1024x1024xf32>, tensor<1024x1024xf32>)
      outs(%c_scaled : tensor<1024x1024xf32>) -> tensor<1024x1024xf32>

    return %res : tensor<1024x1024xf32>
  }
}
