# Matplotlib에서 한글 폰트 설정
# 그래프에서 마이너스 폰트 깨지는 현상 방지
plt.rcParams['axes.unicode_minus'] = False

# Font Path Set
script_dir = os.path.dirname(__file__)
font_path = os.path.join(script_dir, "Fonts", "NanumGothic-Bold.ttf")

if os.path.isfile(font_path):
    font_name = fm.FontProperties(fname=font_path).get_name()
    # weight(폰트 굵기 종류) = 'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'.
    plt.rc('font', family=font_name, size=14, weight='semibold')
    print(f"한글 폰트 '{font_name}'이 설정되었습니다.")
else:
    print("폰트 파일을 찾을 수 없습니다.")
