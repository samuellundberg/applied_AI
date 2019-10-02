function [robot, k] = robot_move(robot, k, T)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    n = length(robot);
    [x, y] = find(robot);
    r_num = rand(1);
    f = @(i,j,k) 4*n*(i-1)+ 4*(j-1) + k;
    T_row = T(f(x,y,k),:);
    poss_moves = find(T_row);
    
    c = 0;
    while r_num > 0
        c = c + 1;
        r_num = r_num - T_row(poss_moves(c));
    end
    %c
    new_pos = poss_moves(c);
    robot(x,y) = 0;
    x = floor(new_pos/(4*n) - 1e-03) + 1;
    y = floor((new_pos-4*n*(x-1))/4 - 1e-03) + 1;
    
    robot(x,y) = 1;
    k = new_pos - 4*n*(x-1) - 4*(y-1);
    
        
    
    

end

