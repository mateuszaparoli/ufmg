// PolyBench-Linalg: 2MM (Two Matrix Multiplications: D = (A x B) x C + D)
// Demonstrates producer-consumer loop fusion in Linalg dialect.

module {
  func.func @kernel_2mm_linalg(
    %alpha: f32,
    %beta: f32,
    %A: tensor<1024x1024xf32>,
    %B: tensor<1024x1024xf32>,
    %C: tensor<1024x1024xf32>,
    %D: tensor<1024x1024xf32>
  ) -> tensor<1024x1024xf32> {
    
    %zero = arith.constant 0.0 : f32
    %init_tmp = tensor.empty() : tensor<1024x1024xf32>
    %tmp_zeroed = linalg.fill ins(%zero : f32) outs(%init_tmp : tensor<1024x1024xf32>) -> tensor<1024x1024xf32>

    // 1. First Matmul: TMP = A x B
    %tmp = linalg.matmul
      ins(%A, %B : tensor<1024x1024xf32>, tensor<1024x1024xf32>)
      outs(%tmp_zeroed : tensor<1024x1024xf32>) -> tensor<1024x1024xf32>

    // 2. Second Matmul: D = TMP x C + D
    %res = linalg.matmul
      ins(%tmp, %C : tensor<1024x1024xf32>, tensor<1024x1024xf32>)
      outs(%D : tensor<1024x1024xf32>) -> tensor<1024x1024xf32>

    return %res : tensor<1024x1024xf32>
  }
}
