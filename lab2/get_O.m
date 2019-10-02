function [O_cell, O] = get_O(O_cell,n,p)
% We firstly simulate which position that will be observed by the sensor.
% If the observed position is new we calculate O and saves it in O_cell.
% If we have already calculated the observed position we re-use
% the O that has been saved in O_Cell.
s = 4*n^2;
O_bin = zeros(n);
O_prob = zeros(n);
O_vec = zeros(1,n*n);
O = zeros(s);

r_num = rand(1);
for i=-2:2
    if r_num < 0
        break
    end
    for j=-2:2
        if(p(1)+i >= 1 & p(1)+i <= n & p(2)+j >=1 & p(2)+j<=n)
            if i == 0 & j == 0
                r_num = r_num - 0.1;
                if r_num < 0
                    O_bin(p(1)+i,p(2)+j) = 1;
                    break
                end
            elseif abs(i)<2 & abs(j)<2
                r_num = r_num - 0.05;
                if r_num < 0
                    O_bin(p(1)+i,p(2)+j) = 1;
                    break
                end
            else
                r_num = r_num - 0.025;
                if r_num < 0
                    O_bin(p(1)+i,p(2)+j) = 1;
                    break
                end

            end 
        end
    end
end

if r_num < 0 
    [px,py] = find(O_bin);
    if isempty(O_cell{n*(px-1) + py})
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
        O_cell{n*(px-1) + py} = O;    
    else
        O = O_cell{n*(px-1) + py};
    end
else
    O = O_cell{n^2+1};
end
end
