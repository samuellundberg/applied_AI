%HMM
% The main method. Here we initiate f,T,O, the robot 
% and then iterates the forward filtering
n = 5;
s = 4 * n^2;
steps = 1e4;
T = get_T(n,s);

O_cell = {};
O_cell{n^2 + 1} = O_dead_sensor(n,s);

robot = zeros(n);
x0 = randi(5);
y0 = randi(5);
robot_dir = randi(4);
robot(x0,y0) = 1;

f = ones(s,1)./s;
state = @(i,j,k) 4*n*(i-1) + 4*(j-1) + k;
error = zeros(steps,1);
for i = 1:steps
    [robot, robot_dir] = robot_move(robot, robot_dir, T);
    [rx, ry] = find(robot);
    robot_pos = [rx, ry];
    % Updates the storage of  O-matrices and gives the current one
    [O_cell, O_t] = get_O(O_cell, n, robot_pos);
    alpha = 1/norm(O_t*T'*f, 1);
    f = alpha*O_t*T'*f;
    
    f_small = sum(vec2mat(f,4), 2);
    fmat = vec2mat(f_small,n);
    [fx, fy] = find(fmat == max(f_small));
    fx = round(mean(fx));
    fy = round(mean(fy));
    error(i) = abs(fx-rx) + abs(fy-ry);
    
% Plot of the ground truth robot and f for comparison
% Takes time so dont do it for to many iterations

%     subplot(1,2,1)
%     imagesc(fmat)
%     title(['probability for robot location', num2str(error(i))])
%     colorbar
%     caxis([0, 1])
% 
%     subplot(1,2,2)
%     imagesc(robot)
%     title('ground truth')
%     colorbar
%     pause(0.2)
end

% konverges to about 0.33 and 1.8
success_rate = sum(error == 0)/steps
mean_err = mean(error)
    