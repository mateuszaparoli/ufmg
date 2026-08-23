// Normalized and Fixed SYMM Kernel (Compatible with MLIR 20.1 Pipelines)
module {
  #map_triangular = affine_map<(d0) -> (d0)>
  
  func.func @kernel_symm_fixed(
    %M: index, %N: index,
    %alpha: f64, %beta: f64,
    %C: memref<1024x1024xf64>,
    %A: memref<1024x1024xf64>,
    %B: memref<1024x1024xf64>
  ) {
    affine.for %i = 0 to 1024 {
      affine.for %j = 0 to 1024 {
        // Step 1: Scale diagonal/current C element
        %c_val = affine.load %C[%i, %j] : memref<1024x1024xf64>
        %c_beta = arith.mulf %c_val, %beta : f64
        affine.store %c_beta, %C[%i, %j] : memref<1024x1024xf64>

        // Step 2: Canonical triangular reduction loop with explicit affine map bound
        affine.for %k = 0 to #map_triangular(%i) {
          %a_ik = affine.load %A[%i, %k] : memref<1024x1024xf64>
          %b_kj = affine.load %B[%k, %j] : memref<1024x1024xf64>
          %term = arith.mulf %a_ik, %b_kj : f64
          %term_alpha = arith.mulf %term, %alpha : f64

          %curr = affine.load %C[%i, %j] : memref<1024x1024xf64>
          %updated = arith.addf %curr, %term_alpha : f64
          affine.store %updated, %C[%i, %j] : memref<1024x1024xf64>
        }
      }
    }
    return
  }
}
