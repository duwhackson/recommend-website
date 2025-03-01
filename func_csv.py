import pandas as pd
import os


def print_full_data():
    """
    打印完整数据，不省略
    """
    # 设置 pandas 显示选项，不省略数据
    pd.set_option('display.max_rows', None)  # 显示所有行
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', None)  # 自动调整显示宽度
    pd.set_option('display.max_colwidth', None)  # 显示完整的列内容

    print(f"当前工作目录: {os.getcwd()}")
    print(f"检查web.csv是否存在: {os.path.exists('web.csv')}")

    try:
        # 尝试使用不同编码读取
        for encoding in ['cp1252', 'latin1', 'utf-8']:
            try:
                df = pd.read_csv('web.csv', encoding=encoding)
                print(f"成功使用 {encoding} 编码读取文件")

                # 打印所有数据（不省略）
                print("\n完整数据帧:")
                print(df)

                # 打印特定流派的数据
                print("\n所有不同的GENRE值:")
                genres = df['GENRE'].dropna().unique()
                for g in genres:
                    print(f"- {g}")

                # 统计每个流派的数量
                print("\n每个流派的行数:")
                print(df['GENRE'].value_counts())

                # 仅打印Kpop数据
                print("\nKpop相关数据:")
                kpop_data = df[df['GENRE'].str.contains('Hip', case=False) &
                               df['GENRE'].str.contains('Hop', case=False)]

                if len(kpop_data) > 0:
                    print(f"找到 {len(kpop_data)} 行Kpop数据:")
                    print(kpop_data)
                else:
                    print("未找到Kpop数据")

                return
            except Exception as e:
                print(f"使用 {encoding} 编码时出错: {e}")
                continue

        print("无法读取文件")
    except Exception as e:
        print(f"总体错误: {e}")


if __name__ == "__main__":
    print_full_data()