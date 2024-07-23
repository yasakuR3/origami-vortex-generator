clearvars
close all

% データが保存されているフォルダのパス
data_folder = 'C:\Users\fml_user\Desktop\drive-download-20240716T123437Z-001';

rho = 1.2; % 空気密度 [kg/m^3]

% 差圧 [Pa] のリスト
dp = [0, 3.2, 8.4, 10.5, 12.5, 16.4, 20.1, 23.1, 28.0, 30.5, 38.3, 44.0, 49.7, 58.6, 69.6, 79.5, 89.0, 100.95, 101.55, 115.0];

% 差圧から速度を計算
U = sqrt(2*dp/rho);

% 平均電圧を格納するための配列
aveE = zeros(1, length(dp));

% 各ファイルを読み込み、平均電圧を計算
for i = 1:length(dp)
    fn = sprintf('%d.mat', i); % シンプルなファイル名を生成
    full_fn = fullfile(data_folder, fn); % フルパスを生成
    load(full_fn, 'data'); % 'data' 変数をロード
    aveE(i) = mean(data); % 平均電圧を計算
end

% 3次の多項式フィットを行う
coef = polyfit(aveE, U, 3);

% フィットした曲線をプロットするための範囲を設定
x = linspace(min(aveE), max(aveE), 100);
y = polyval(coef, x);

% プロット
figure; hold on
plot(aveE, U, 'o') % 測定データをプロット
plot(x, y) % フィットした曲線をプロット
legend('計測点', '3次近似式')
xlabel('平均電圧 (V)')
ylabel('流速 [m/s]')
title('電圧と流速の関係')

% 結果を表示
disp('Coefficients of the polynomial fit:');
disp(coef);
