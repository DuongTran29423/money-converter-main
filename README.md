# money-converter


```
.
├── static 
├── templates 
└── main.py 
```

## Cấu trúc file

### static 🤝 🙏🏻

Các resources tĩnh, chủ yếu dùng để làm đẹp giao diện cho web

### templates 🤝 🧠

Phần giao diện của web, với data được đổ lên từ server

### main.py ✍🏻 🧠

Server python

## Cách server hoạt động ✍🏻 🧠

```py
from flask import Flask, render_template, request

app = Flask(__name__)

# define route để vào app và method hỗ trợ
# route "/" nghĩa là vào thẳng từ domain (vd: http://127.0.0.1:5000/)
# method "GET" và "POST": "GET" sử dụng khi truy cập thẳng lần đầu, "POST" sử dụng sau khi submit form để xử lý kết quả
@app.route("/", methods=["GET", "POST"])
def home():
    # dữ liệu tỷ giá (code cứng, không tự update)
    curs = ["USD", "EUR", "GBP"]
    cur_values = [24830, 26266, 30426]

    # nếu là method là "POST", tức là đang xử lý cho trường hợp sau khi submit form
    if request.method == "POST":
        # lấy dữ liệu từ input "source-input", sau đó đổi từ string thành int
        src_input = int(request.form['source-input'])
        # lấy dữ liệu từ input "currency"
        currency = request.form['currency']
        # tìm trong dữ liệu cứng ở trên, index của tỷ giá được chọn, sử dụng array.index()
        index = curs.index(currency)
        # lấy user input nhân với giá trị của tỷ giá, được lấy dựa theo index vừa tìm được ở trên
        result = src_input * cur_values[index]
        # đẩy các dữ liệu và kết quả tính toán được lên giao diện
        return render_template('index.html', result=result, prev_input=src_input, curs=curs, cur_values=cur_values)

    # nếu method là "GET", tức đang xử lý cho trường hợp mới vào lần đầu, chưa xử lý tính toán gì
    else:
        # đẩy dữ liệu lên trên giao diện
        return render_template('index.html', curs=curs, cur_values=cur_values)


if __name__ == "__main__":
    app.run(debug=True)

```

## Cách giao diện hoạt động 🤝 🧠

Tạm chia giao diện thành 3 phần

### Phần headline

Code cứng. Nếu cần sửa thì vào trong [index.html](./templates/index.html), ctrl + F tìm text rồi tự sửa, chỉ nên sửa text không nên sửa html, trừ khi biết mình đang làm gì

### Phần quy đổi

-   Giao diện thì "tụi con copy trên mạng / nhờ người chỉ, chỉ sửa name của các input để gọi xuống dưới python xử lý" (nếu tự tin khoe cá tính thì đọc code rồi tự chém luôn, bảo là con tự làm dựa trên [Bootstrap](https://getbootstrap.com/))
-   Input thứ nhất, có name là `source-input`, được dùng để gọi xuống python và thu thập dưới tên biến là `src_input`

```py
src_input = int(request.form['source-input'])
```

-   Sau khi submit form quy đổi, sẽ gây ra tình trạng reload lại trang, gây mất giá trị của input. Giá trị này sau đó được khôi phục bằng cách lấy giá trị của `src_input`

```py
return render_template('index.html', ..., prev_input=src_input, ...)
```

```html
<input
    type="number"
    class="form-control"
    name="source-input"
    {% if prev_input %} value="{{ prev_input }}" {% endif %}
/>
```

-   Input thứ 2, là readonly, chỉ render kết quả, không nhập được, hiện app chỉ hỗ trợ quy đổi 1 chiều
-   Nút `Quy đổi` là để submit form
-   Nút `Nhập lại` là để reset form

### Phần bảng tỷ giá

Lấy dữ liệu từ `curs` và `cur_values` đẩy lên từ server python

```py
return render_template('index.html', ..., curs=curs, cur_values=cur_values)
```

```html
<table class="table mt-5">
    <!-- Headline -->
    <thead>
        <tr>
            <th scope="col">Đơn vị</th>
            <th scope="col">Tỷ giá</th>
        </tr>
    </thead>
    <!-- Phần thân, được chạy for loop để tạo hàng ứng với các tỷ giá -->
    <tbody>
        <!-- Duyệt qua mảng curs -->
        {% for c in curs %}
        <tr>
            <!-- Xuất các item trong curs ra để làm cột "Đơn vị" -->
            <th scope="row">{{ c }}</th>
            <!-- Lấy item trong cur_values ứng với index hiện tại trong for loop để làm cột "Tỷ giá" -->
            <td>{{ cur_values[loop.index - 1] }}</td>
        </tr>
        <!-- Kết thúc for loop -->
        {% endfor %}
    </tbody>
</table>
```
