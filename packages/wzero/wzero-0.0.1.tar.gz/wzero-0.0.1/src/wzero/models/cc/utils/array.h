#ifndef ARRAY_H
#define ARRAY_H

#include <vector>

template <class T>
class Array1D {
public:

    T* data;
    int size;
    bool alloced_memory;

    Array1D(int size) {
        this->data = new T[size]();
        this->size = size;
        this->alloced_memory = true;
    };

    Array1D(T* data, int size) {
        this->data = data;
        this->size = size;
        this->alloced_memory = false;
    };

    T sum() {
        T sum = 0;
        for(int i = 0; i < this->size; ++i)
            sum += this->data[i];
        return sum;
    };

    T& operator[](int i) {
        return this->data[i];
    };

    ~Array1D() {
        if (this->alloced_memory)
            delete [] this->data;
    };

};


template <class T>
class Array2D {
public:

    T* data;
    int shape[2];
    bool alloced_memory;

    Array2D(int x, int y) {
        this->data = new T[x*y]();
        this->shape[0] = x;
        this->shape[1] = y;
        this->alloced_memory = true;
    };

    Array2D(T* data, int x, int y) {
        this->data = data;
        this->shape[0] = x;
        this->shape[1] = y;
        this->alloced_memory = false;
    };

    T& operator[](int i) {
        return this->data[i];
    };

    T& operator()(int x, int y) {
        return this->data[this->shape[1]*x + y];
    };

    ~Array2D() {
        if (this->alloced_memory)
            delete [] this->data;
    };

};

template <class T, unsigned int N>
class ArrayND {
public:

    T* data;
    int shape[N];
    bool alloced_memory;

    template <typename ...A>
    ArrayND(A... args) {
        std::vector<int> dims = {args...};
        int size = 1;
        for(size_t i = 0; i < dims.size(); ++i) {
            this->shape[i] = dims[i];
            size *= dims[i];
        }
        this->data = new T[size]();
        this->alloced_memory = true;
    };

    template <typename ...A>
    ArrayND(T* data, A... args) {
        std::vector<int> dims = {args...};
        for(size_t i = 0; i < dims.size(); ++i)
            this->shape[i] = dims[i];
        this->data = data;
        this->alloced_memory = false;
    };

    T& operator[](int i) {
        return this->data[i];
    };

    template <typename ...A>
    T& operator()(A... args) {
        std::vector<int> indexs = {args...};
        int index = 0;
        int prod;
        for(size_t i = 0; i < N; ++i) {
            prod = indexs[i];
            for(size_t j = i; j < N; ++j)
                prod *= this->shape[j];
            index += prod;
        };
        return this->data[index];
    };

    ~ArrayND() {
        if (this->alloced_memory)
            delete [] this->data;
    };

};

#endif