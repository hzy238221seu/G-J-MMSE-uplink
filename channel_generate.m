function [H,Hhat,C,Epsilon] = channel_generate(L, N, K, p, tau_c, tau_p)
    %% Define simulation setup

    %Number of setups with random UE locations
    nbrOfSetups = 1;
    %nbrOfSetups = 1;

    % %Number of APs in the cell-free network
    % L = 100;

    % %Number of UEs in the network
    % K = 40;

    % %Number of antennas per AP
    % N = 4;

    % %Length of the coherence block
    % tau_c = 200;

    % %Compute number of pilots per coherence block
    % tau_p = 10;

    % %Uplink transmit power per UE (mW)
    % p = 100;

    %% Go through all setups
    for n = 1:nbrOfSetups
        %Generate one setup with UEs at random locations
        [R,~,pilotIndex,~] = generateSetup(L,K,N,100,1);

        %Generate channel realizations, channel estimates, and estimation
        %error correlation matrices for all UEs to the cell-free APs
        [Hhat,H,B] = functionChannelEstimates(R,1,L,K,N,tau_p,pilotIndex,p);
        shape_H = size(H);
        H = reshape(H, shape_H(1), shape_H(3));
        Hhat = reshape(Hhat, shape_H(1), shape_H(3));
        C_s = permute(R-B, [4, 3, 1, 2]);
        C = zeros(K, L*N, L*N);
        for i = 1:L
            C(:, (i-1)*N+1:i*N, (i-1)*N+1:i*N) = C_s(:, i, :, :);
        end
        Epsilon = Hhat * transpose(conj(Hhat));
        % save([['E:\\data\\L100N4K40-heterogeneous\\', num2str(n)], '.mat'], "H", "Hhat", "C", "Epsilon");
    end