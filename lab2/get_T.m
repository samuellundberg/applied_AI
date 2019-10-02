function [T] = get_T(n,s)
% loops through each position in the matrix. Each position has for states.
% For each state the probability to go from state i to state j is
% calculated and inserted at index i,j in T.
% To catch every case set_Tx is awfull functions full of if_statements.
T = zeros(s);
f = @(i,j,k) 4*n*(i-1)+ 4*(j-1) + k;
for i = 1:n
    for j = 1:n
        T = set_T1(T,i,j,f,n);
        T = set_T2(T,i,j,f,n);
        T = set_T3(T,i,j,f,n);
        T = set_T4(T,i,j,f,n);
    end
end

%spy(T)