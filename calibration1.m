clearvars
close all

% データが保存されているフォルダのパス
data_folder = 'C:\Users\fml_user\Desktop\origami-vortex generator\実験データ\20241004_風洞実験\キャリブレーション';

rho = 1.293; % 空気密度 [kg/m^3]

% 差圧 [Pa] のリスト
dp = [0, 1.45, 7.2, 17.2, 31, 48.6, 70, 95, 126, 160, 192];

% 差圧から速度を計算する。
U = sqrt(2 * dp / rho);

% 平均電圧を格納するための配列
aveE = zeros(1, length(dp));

% 各ファイルを読み込み、平均電圧を計算する。
for i = 1:length(dp)
    fn = sprintf('%gPa.mat', dp(i)); % 差圧に基づくファイル名を生成する。
    full_fn = fullfile(data_folder, fn); % フルパスを生成する。
    load(full_fn, 'data'); % 'data' 変数を読み取る。
    aveE(i) = mean(data); % 平均電圧を計算する。
end

% 4次の多項式フィットを行う。
coef = polyfit(aveE, U, 4);

% フィットした曲線をプロットするための範囲を設定する。
x = linspace(min(aveE), max(aveE), 100);
y = polyval(coef, x);

% プロット
figure; hold on
plot(aveE, U, 'o', 'MarkerSize', 8) % 測定データをプロット
plot(x, y, 'LineWidth', 2) % フィットした曲線をプロット
legend('計測点', '4次近似式', 'FontSize', 14)
xlabel('平均電圧[V]', 'FontSize', 14)
ylabel('流速[m/s]', 'FontSize', 14)
title('電圧[V]と流速[m/s]の関係', 'FontSize', 16)
set(gca, 'FontSize', 12) % 軸のラベルや目盛りのフォントサイズを設定

% 係数を表示
disp('4次近似式の係数は以下の通りです：');
disp(coef);

