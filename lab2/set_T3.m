function [T] = set_T3(T,i,j,f,n)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    k = 3;
    if i == 1
        T(f(i,j,k), f(i+1,j,k)) = 0.7;
        if j == 1
            T(f(i,j,k), f(i,j+1,2)) = 0.3;
        elseif j < n
            T(f(i,j,k), f(i,j+1,2)) = 0.15;
            T(f(i,j,k), f(i,j-1,4)) = 0.15;
        else
            T(f(i,j,k), f(i,j-1,4)) = 0.3;
        end
    elseif i < n
        T(f(i,j,k), f(i+1,j,k)) = 0.7;
        if j == 1
            T(f(i,j,k), f(i-1,j,1)) = 0.15;
            T(f(i,j,k), f(i,j+1,2)) = 0.15;
        elseif j < n
            T(f(i,j,k), f(i-1,j,1)) = 0.1;
            T(f(i,j,k), f(i,j+1,2)) = 0.1;
            T(f(i,j,k), f(i,j-1,4)) = 0.1;
        else
            T(f(i,j,k), f(i-1,j,1)) = 0.15;
            T(f(i,j,k), f(i,j-1,4)) = 0.15;
        end
    else
        if j == 1
            T(f(i,j,k), f(i-1,1,1)) = 0.5;
            T(f(i,j,k), f(i,j+1,2)) = 0.5;
        elseif j < n
            T(f(i,j,k), f(i-1,j,1)) = 1/3;
            T(f(i,j,k), f(i,j+1,2)) = 1/3;
            T(f(i,j,k), f(i,j-1,4)) = 1/3;
        else
            T(f(i,j,k), f(i-1,j,1)) = 0.5;
            T(f(i,j,k), f(i,j-1,4)) = 0.5;
        end

    end

end