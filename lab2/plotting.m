% getting the plots
%% plotting T
n = 5;
s = 4 * n^2;
T = get_T(n,s);
% subplot(1,2,1)
spy(T)
% subplot(1,2,2)
figure
imagesc(T)
colorbar
axis equal
axis tight

%%
n = 5;
s = 4 * n^2;
p = [1,5];
px=p(1);
py=p(2);
% O_cell = {};
% O_cell{n^2 + 1} = O_dead_sensor(n,s);
Od = O_dead_sensor(n,s);
% [O_cell, O] = get_O(O_cell,n,p)
O_prob = zeros(n);
O_vec = zeros(1,n*n);
O = zeros(s);

for i=-2:2
    for j=-2:2
        if px+i >= 1 & px+i <= n & py+j >= 1 & py+j <= n
            if abs(i) < 2 & abs(j) < 2
                O_prob(px+i,py+j)=0.05;
            elseif abs(i) == 2 || abs(j) == 2
                O_prob(px+i,py+j)=0.025;
            end 
        end
    end
end
O_prob(px, py) = 0.1;
for i = 1:n
    O_vec(1+(i-1)*n:i*n) = O_prob(i,:);
end
for i = 1:s
    O(i,i) = O_vec(floor(i/4 - 1e-02)+1);
end

    



%spy(Od)
figure
imagesc(Od)
colorbar
%figure
%spy(O)
figure
imagesc(O)
colorbar
%%

x = 3; y = 3;
dist = 0;
for i = 1:5
    for j = 1:5
        dist = dist + abs(x-i) + abs(x-j);
    end
end
dist/25



