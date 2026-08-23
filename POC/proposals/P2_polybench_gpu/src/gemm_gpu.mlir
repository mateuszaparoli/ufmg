// MLIR GPU Dialect Kernel for General Matrix Multiplication (GEMM)
// Demonstrates Affine to GPU lowering with thread block tiling and shared memory caching.

module attributes {gpu.container_module} {
  gpu.module @gemm_cuda_kernel {
    gpu.func @kernel_gemm_gpu(%A: memref<1024x1024xf32>, %B: memref<1024x1024xf32>, %C: memref<1024x1024xf32>, %alpha: f32, %beta: f32)
      workgroup(%bx : index, %by : index, %bz : index)
      private(%tx : index, %ty : index, %tz : index)
      kernel {
      
      // Calculate global row and column indices
      %block_size_x = arith.constant 16 : index
      %block_size_y = arith.constant 16 : index
      
      %bx_offset = arith.muli %bx, %block_size_x : index
      %by_offset = arith.muli %by, %block_size_y : index
      
      %row = arith.addi %by_offset, %ty : index
      %col = arith.addi %bx_offset, %tx : index
      
      // Allocate shared memory tiles (16x16 elements per thread block)
      %sh_A = memref.alloca() : memref<16x16xf32, 3> // Address space 3 = Shared Memory
      %sh_B = memref.alloca() : memref<16x16xf32, 3>
      
      %zero = arith.constant 0.0 : f32
      %sum_init = arith.constant 0.0 : f32
      
      // Accumulator in GPU register
      %c_init = memref.alloca() : memref<1xf32>
      memref.store %zero, %c_init[%zero] : memref<1xf32>
      
      %num_tiles = arith.constant 64 : index // 1024 / 16 = 64 tiles
      
      scf.for %tile_idx = %zero to %num_tiles step %zero {
        // 1. Cooperative load from Global Memory to Shared Memory
        %k_A = arith.addi %tile_idx, %tx : index
        %val_A = memref.load %A[%row, %k_A] : memref<1024x1024xf32>
        memref.store %val_A, %sh_A[%ty, %tx] : memref<16x16xf32, 3>
        
        %k_B = arith.addi %tile_idx, %ty : index
        %val_B = memref.load %B[%k_B, %col] : memref<1024x1024xf32>
        memref.store %val_B, %sh_B[%ty, %tx] : memref<16x16xf32, 3>
        
        // 2. Synchronize all threads within workgroup
        gpu.barrier
        
        // 3. Compute partial dot product from Shared Memory
        scf.for %k = %zero to %block_size_x step %zero {
          %a = memref.load %sh_A[%ty, %k] : memref<16x16xf32, 3>
          %b = memref.load %sh_B[%k, %tx] : memref<16x16xf32, 3>
          %prod = arith.mulf %a, %b : f32
          %curr = memref.load %c_init[%zero] : memref<1xf32>
          %updated = arith.addf %curr, %prod : f32
          memref.store %updated, %c_init[%zero] : memref<1xf32>
        }
        
        // 4. Synchronize before loading next tile
        gpu.barrier
      }
      
      // 5. Store back to Global Memory
      %final_sum = memref.load %c_init[%zero] : memref<1xf32>
      %alpha_scaled = arith.mulf %final_sum, %alpha : f32
      %orig_c = memref.load %C[%row, %col] : memref<1024x1024xf32>
      %beta_c = arith.mulf %orig_c, %beta : f32
      %result = arith.addf %alpha_scaled, %beta_c : f32
      memref.store %result, %C[%row, %col] : memref<1024x1024xf32>
      
      gpu.return
    }
  }

  // Host Launch Wrapper
  func.func @launch_gemm(%A: memref<1024x1024xf32>, %B: memref<1024x1024xf32>, %C: memref<1024x1024xf32>, %alpha: f32, %beta: f32) {
    %c64 = arith.constant 64 : index // Grid dimensions (64x64 blocks)
    %c16 = arith.constant 16 : index // Block dimensions (16x16 threads = 256 threads/block)
    %c1 = arith.constant 1 : index
    
    gpu.launch_func @gemm_cuda_kernel::@kernel_gemm_gpu
      blocks in (%c64, %c64, %c1)
      threads in (%c16, %c16, %c1)
      args(%A : memref<1024x1024xf32>, %B : memref<1024x1024xf32>, %C : memref<1024x1024xf32>, %alpha : f32, %beta : f32)
    return
  }
}
