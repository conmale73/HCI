from django.contrib import admin
#from .models import Product, Variation, ReviewRating
from .models import Product, ReviewRating
from django_ckeditor_5.widgets import CKEditor5Widget

# Quản trị viên sản phẩm
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    class Meta:
          model = Product
          fields = ("author", "text")
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          }

# Quản trị viên biến thể
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_editable = ('is_active',)   # Cho phép chỉnh sửa trên list hiển thị
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
#admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
