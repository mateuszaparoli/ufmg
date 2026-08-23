// Broken/Un-normalized SYMM Kernel
module {
  func.func @kernel_symm_broken(%M: index, %N: index, %alpha: f64, %beta: f64,
                                %C: memref<1024x1024xf64>, %A: memref<1024x1024xf64>, %B: memref<1024x1024xf64>) {
    affine.for %i = 0 to %M {
      affine.for %j = 0 to %N {
        %acc = memref.alloca() : memref<1xf64>
        // Triangular dependency that confuses greedy fusion
        affine.for %k = 0 to %i {
          %a_val = affine.load %A[%i, %k] : memref<1024x1024xf64>
          %b_val = affine.load %B[%k, %j] : memref<1024x1024xf64>
          %prod = arith.mulf %a_val, %b_val : f64
          // Multiple non-affine writes to different rows in the same inner iteration
          %c_curr = affine.load %C[%k, %j] : memref<1024x1024xf64>
          %c_new = arith.addf %c_curr, %prod : f64
          affine.store %c_new, %C[%k, %j] : memref<1024x1024xf64>
        }
      }
    }
    return
  }
}
