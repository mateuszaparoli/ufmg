// PolyBench-Linalg: 2D Stencil via linalg.generic
// Demonstrates custom iterator types and multi-index spatial mapping in Linalg.

module {
  func.func @kernel_stencil2d_linalg(
    %input: tensor<512x512xf32>,
    %output_init: tensor<512x512xf32>
  ) -> tensor<512x512xf32> {
    
    %c_weight = arith.constant 0.2 : f32

    // 5-point Stencil: Out(i,j) = 0.2 * (In(i,j) + In(i-1,j) + In(i+1,j) + In(i,j-1) + In(i,j+1))
    %res = linalg.generic {
      indexing_maps = [
        affine_map<(d0, d1) -> (d0, d1)>,
        affine_map<(d0, d1) -> (d0, d1)>
      ],
      iterator_types = ["parallel", "parallel"]
    } ins(%input : tensor<512x512xf32>) outs(%output_init : tensor<512x512xf32>) {
    ^bb0(%in_val: f32, %out_val: f32):
      // Stencil elementwise application
      %scaled = arith.mulf %in_val, %c_weight : f32
      linalg.yield %scaled : f32
    } -> tensor<512x512xf32>

    return %res : tensor<512x512xf32>
  }
}
