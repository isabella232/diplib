%CONVOLVE   General convolution filter
%
% SYNOPSIS:
%  image_out = convolve(image_in,kernel,boundary_condition)
%
%  If KERNEL is separable, the convolution is computed in the spatial
%  domain using NDIMS(IMAGE_IN) one-dimensional convolutions. If not, the
%  convolution is computed either through the Fourier Domain or by direct
%  implementation of the convolution sum, depending on the size of the kernel.
%  The function uses the number of pixels in the kernel and the number of
%  pixels in the image to determine which method is the most efficient.
%  In all cases, the output is the same size as the input image.
%
%  (TODO: everything in the above paragraph is not yet implemented.)
%  Currently: kernel is either:
%  - A cell array with vectors, or a single vector. Each vector describes a
%    1D filter that is applied to a different image dimension. There should
%    be as many vectors as dimensions in IMAGE_IN, or only one to apply it
%    to each dimension. For example:
%
%     a = readim('cermet');
%     convolve(a,{[1,1,1],[-1,0,1]})
%
%  - A struct array with fields 'filter', 'origin' and 'flags'. Each array
%    element describes a 1D filter for a different dimension. There should
%    be as many vectors as dimensions in IMAGE_IN, or only one to apply it
%    to each dimension. The 'filter' field is required, and contains a vector
%    with the filter weights (as in the cell array). The 'origin' field is
%    the index into 'filter' that is the origin of the filter. If it is
%    negative or not given, the origin will be placed at the middle of the
%    filter, or the pixel to the right if the size is even. The 'flags' field
%    contains one of the strings 'general' (or '', or not present), 'even',
%    'odd', 'd-even', or 'd-odd'. These cause the filter weights to be
%    repeated to obtain an even or odd symmetry in the filter. The 'd-'
%    prefix creates an even-sized filter by repeating all weights, otherwise
%    an odd-sized filter is created, in which the right-most weight is not
%    repeated.
%
%  In either case, an empty vector or a vector [1] causes that dimension to
%  not be processed.
%
%  BOUNDARY_CONDITION is a string or a cell array of strings (one per image
%  dimension) specifying how the convolution handles pixel values outside
%  of the image domain.
%
% DEFAULTS:
%  boundary_condition = {} (equivalent to 'mirror')
%
% NOTE:
%  See the user guide for the available boundary condition strings.
%
% DIPlib:
%  This function calls the DIPlib functions dip::SeparableConvolution,
%  dip::ConvolveFT or dip::GeneralConvolution, depending on the input.

% (c)2017, Cris Luengo.
% Based on original DIPlib code: (c)1995-2014, Delft University of Technology.
% Based on original DIPimage code: (c)1999-2014, Delft University of Technology.
%
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
%
%    http://www.apache.org/licenses/LICENSE-2.0
%
% Unless required by applicable law or agreed to in writing, software
% distributed under the License is distributed on an "AS IS" BASIS,
% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
% See the License for the specific language governing permissions and
% limitations under the License.