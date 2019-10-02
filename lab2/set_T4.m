function [T] = set_T4(T,i,j,f,n)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    k = 4;
    if j == 1
        if i == 1
            T(f(i,j,k), f(i,j+1,2)) = 0.5;
            T(f(i,j,k), f(i+1,j,3)) = 0.5;
        elseif i < n
            T(f(i,j,k), f(i-1,j,1)) = 1/3;
            T(f(i,j,k), f(i+1,j,3)) = 1/3;
            T(f(i,j,k), f(i,j+1,2)) = 1/3;
        else
            T(f(i,j,k), f(i,j+1,2)) = 0.5;
            T(f(i,j,k), f(i-1,j,1)) = 0.5;
        end
    elseif j < n
        T(f(i,j,k), f(i,j-1,k)) = 0.7;
        if i == 1
            T(f(i,j,k), f(i,j+1,2)) = 0.15;
            T(f(i,j,k), f(i+1,j,3)) = 0.15;
        elseif i < n
            T(f(i,j,k), f(i-1,j,1)) = 0.1;
            T(f(i,j,k), f(i,j+1,2)) = 0.1;
            T(f(i,j,k), f(i+1,j,3)) = 0.1;
        else
            T(f(i,j,k), f(i,j+1,2)) = 0.15;
            T(f(i,j,k), f(i-1,j,1)) = 0.15;
        end
    else
        T(f(i,j,k), f(i,j-1,k)) = 0.7;
        if i == 1
            T(f(i,j,k), f(i+1,j,3)) = 0.3;
        elseif i < n
            T(f(i,j,k), f(i-1,j,1)) = 0.15;
            T(f(i,j,k), f(i+1,j,3)) = 0.15;
        else
            T(f(i,j,k), f(i-1,j,1)) = 0.3;
        end
    end
end