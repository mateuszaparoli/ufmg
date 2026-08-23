// MLIR GPU Dialect Kernel for Stencil 2D (FDTD-2D)
// Illustrates stencil spatial neighbor updates across GPU threads with halo exchange.

module attributes {gpu.container_module} {
  gpu.module @fdtd2d_cuda_kernel {
    gpu.func @kernel_fdtd2d_gpu(%ex: memref<1024x1024xf32>, %ey: memref<1024x1024xf32>, %hz: memref<1024x1024xf32>, %tmax: i32)
      workgroup(%bx : index, %by : index, %bz : index)
      private(%tx : index, %ty : index, %tz : index)
      kernel {
      
      %block_x = arith.constant 16 : index
      %block_y = arith.constant 16 : index
      
      %gx = arith.addi %tx, %bx : index
      %gy = arith.addi %ty, %by : index
      
      %c1 = arith.constant 1 : index
      %c1023 = arith.constant 1023 : index
      %half = arith.constant 0.5 : f32
      
      // Boundary check
      %valid_x = arith.cmpi ult, %gx, %c1023 : index
      %valid_y = arith.cmpi ult, %gy, %c1023 : index
      %in_bounds = arith.andi %valid_x, %valid_y : i1
      
      scf.if %in_bounds {
        // Stencil computation: Hz(i,j) = Hz(i,j) - 0.5 * (Ex(i,j+1) - Ex(i,j) + Ey(i+1,j) - Ey(i,j))
        %gy_plus_1 = arith.addi %gy, %c1 : index
        %gx_plus_1 = arith.addi %gx, %c1 : index
        
        %val_ex_next = memref.load %ex[%gx, %gy_plus_1] : memref<1024x1024xf32>
        %val_ex_curr = memref.load %ex[%gx, %gy] : memref<1024x1024xf32>
        %diff_ex = arith.subf %val_ex_next, %val_ex_curr : f32
        
        %val_ey_next = memref.load %ey[%gx_plus_1, %gy] : memref<1024x1024xf32>
        %val_ey_curr = memref.load %ey[%gx, %gy] : memref<1024x1024xf32>
        %diff_ey = arith.subf %val_ey_next, %val_ey_curr : f32
        
        %sum_diff = arith.addf %diff_ex, %diff_ey : f32
        %delta = arith.mulf %half, %sum_diff : f32
        
        %curr_hz = memref.load %hz[%gx, %gy] : memref<1024x1024xf32>
        %new_hz = arith.subf %curr_hz, %delta : f32
        memref.store %new_hz, %hz[%gx, %gy] : memref<1024x1024xf32>
      }
      
      gpu.return
    }
  }
}
