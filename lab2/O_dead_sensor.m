function [O] = O_dead_sensor(n,s)
% Caluculates the O-matrix for when the sensor observes nothing. 
% O(i,j) = probability for sensor reporting nothing when robot is in i,j
% Then O is normalized such that the total probability is 1.
O_small = zeros(n);
O_vec = zeros(1,n*n);
O = zeros(s);

p = [ 1 3 5; 1 5 6; 1 5 9; 1 8 7; 1 8 11; 1 8 16] * [0.1; 0.05; 0.025];
for i = 1:round(n/2+1e-04)
    for j = 1:round(n/2+1e-04)
        if i + j == 2
            O_small(i,j) = p(1);
        elseif i + j == 3
            O_small(i,j) = p(2);
        elseif i + j == 4 && i ~= j
            O_small(i,j) = p(3);
        elseif i + j == 4
            O_small(i,j) = p(4);
        elseif i + j == 5
            O_small(i,j) = p(5);
        else
            O_small(i,j) = p(6);
        end
    end
end
O_small(4, 1:3) = O_small(2,1:3);
O_small(5, 1:3) = O_small(1,1:3);
O_small(:,4) = O_small(:,2);
O_small(:,5) = O_small(:,1);
O_small = 1 - O_small;

for i = 1:n
    O_vec(1+(i-1)*n:i*n) = O_small(i,:);
end
for i = 1:s
    O(i,i) = O_vec(floor(i/4 - 1e-02)+1);
end
O = O / sum(O(:));

end

