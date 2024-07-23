% ディレクトリ内のファイルリストを取得
files = dir('C:\Users\fml_user\Desktop\drive-download-20240722T154949Z-001\*.mat');

% データを保存するための変数
num_files = numel(files);
x_coords = zeros(num_files, 1);
y_coords = zeros(num_files, 1);
mean_ryusoku = zeros(num_files, 1);

% 各ファイルのデータを読み込み
for k = 1:num_files
    file_path = fullfile(files(k).folder, files(k).name);
    data_struct = load(file_path);
    field_names = fieldnames(data_struct);
    data = data_struct.(field_names{1});

    % 平均電圧[V]から流速[m/s]を計算する
    mean_voltage = mean(data);
    mean_ryusoku(k) = 3.4474 * mean_voltage^3 - 13.980 * mean_voltage^2 + 11.3289 * mean_voltage + 6.0496;

    % ファイル名からx座標とy座標を求める。
    file_name = files(k).name;
    tokens = regexp(file_name, 'data_(\d+)_(\d+)_(\d+).mat', 'tokens');
    if ~isempty(tokens)
        y_coords(k) = 10 * (1 - str2double(tokens{1}{1}));
        x_coords(k) = -10 * (1 - str2double(tokens{1}{2}));
    end
end

% 補間用のメッシュグリッドを作成
[x_grid, y_grid] = meshgrid(linspace(min(x_coords), max(x_coords), 100), ...
                             linspace(min(y_coords), max(y_coords), 100));

% データの補間
z_grid = griddata(x_coords, y_coords, mean_ryusoku, x_grid, y_grid, 'cubic');

% サーフェスプロット
figure;
surf(x_grid, y_grid, z_grid, 'EdgeColor', 'none');
xlabel('X座標[mm]');
ylabel('Y座標[mm]');
zlabel('平均流速[m/s]');
title('平均流速分布');
colorbar;
grid on;

% 等高線プロット
figure;
contourf(x_grid, y_grid, z_grid, 20, 'LineColor', 'none');
xlabel('X座標[mm]');
ylabel('Y座標[mm]');
title('平均流速分布の等高線');
colorbar;
