% ディレクトリ内のファイルリストを取得
files = dir('C:\Users\fml_user\Desktop\drive-download-20240722T154949Z-001\*.mat');

% データを保存するための変数
num_files = numel(files);
x_coords = zeros(num_files, 1);
y_coords = zeros(num_files, 1);
mean_ryusoku = zeros(num_files, 1);

% データ全体を保存する
all_data = [];

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

    % 全データに追加
    all_data = [all_data; mean_ryusoku(k)];
end

% 結果の表示
disp('x[mm]座標とy座標[mm]と平均流速[m/s]:');
result_table = table(x_coords, y_coords, mean_ryusoku);
disp(result_table);

% データ全体の統計量を計算
mean_velocity = mean(all_data);
std_velocity = std(all_data);
turbulence_intensity = std_velocity / mean_velocity;

% 結果の表示
fprintf('全データの平均流速[m/s]: %.2f\n', mean_velocity);
fprintf('全データの流速の標準偏差: %.2f\n', std_velocity);
fprintf('全データの乱流強度: %.2f\n', turbulence_intensity);
