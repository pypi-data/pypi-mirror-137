#ifndef TRT_IMAGE_HPP
#define TRT_IMAGE_HPP
#include <vector>

namespace TRT{

class Size{
public:
    Size() = default;
    Size(int width, int height){
        this->width = width;
        this->height = height;
    }

    int width = 0;
    int height = 0;
};

class Image{
public:
    Image() = default;
    Image(int rows, int cols, const void* pdata){
        this->width_ = cols;
        this->height_ = rows;
        this->rows = rows;
        this->cols = cols;
        this->pdata_ = (unsigned char*)(pdata);
    }

    const int width() const{ return width_; }
    const int height() const{ return height_; }
    const unsigned char* data() const{ return pdata_; }
    const Size size() const{ return Size(width_, height_); }
    const bool empty() const{ return this->pdata_ == nullptr || this->width_ == 0 || this->height_ == 0; }

public:
    int rows = 0;
    int cols = 0;

private:
    int width_ = 0;
    int height_ = 0;
    unsigned char* pdata_ = nullptr;
};

inline void invertAffineTransform(float imat[6], float omat[6]){

    float i00 = imat[0];  float i01 = imat[1];  float i02 = imat[2];
    float i10 = imat[3];  float i11 = imat[4];  float i12 = imat[5];

    float D = i00 * i11 - i01 * i10;
    D = D != 0 ? 1.0 / D : 0;

    float A11 = i11 * D;
    float A22 = i00 * D;
    float A12 = -i01 * D;
    float A21 = -i10 * D;
    float b1 = -A11 * i02 - A12 * i12;
    float b2 = -A21 * i02 - A22 * i12;
    omat[0] = A11;  omat[1] = A12;  omat[2] = b1;
    omat[3] = A21;  omat[4] = A22;  omat[5] = b2;
}

template<typename cvmat>
Image cvmat2image(const cvmat& m){

    Image output;
    if(m.empty()){
        printf("Image is empty\n");
        return output;
    }

    const int cv_8u = 0;
    if(!(m.channels() == 3 && m.depth() == cv_8u)){
        printf("Invalid image format, channels = %d, depth = %d, shape = %d x %d\n", m.channels(), m.depth(), m.rows, m.cols);
        return output;
    }

    if(m.step[0] != m.cols * 3){
        printf("Invalid image format, line step mismatch.");
        return output;
    }
    return Image(m.rows, m.cols, m.data);
}

template<typename cvmat>
inline std::vector<Image> cvmat2image(const std::vector<cvmat>& images){
    std::vector<Image> result(images.size());
    for(int i = 0; i < images.size(); ++i){
        result[i] = cvmat2image(images[i]);
    }
    return result;
}

}; // namespace TRT

#endif // TRT_IMAGE_HPP