# Generated by Django 4.2.6 on 2023-11-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0017_modelpagemodel_alter_modelnewsmodel_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelFieldModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_id", models.IntegerField(default=0, verbose_name="模型")),
                (
                    "field_title",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="字段名称"
                    ),
                ),
                (
                    "field_key",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="字段Key"
                    ),
                ),
                ("field_type", models.IntegerField(default=0, verbose_name="字段类型")),
                ("field_length", models.IntegerField(default=0, verbose_name="最大输入长度")),
                (
                    "field_upload_type",
                    models.IntegerField(default=0, verbose_name="上传类型"),
                ),
                (
                    "field_default",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="默认值"
                    ),
                ),
                (
                    "field_list",
                    models.TextField(blank=True, null=True, verbose_name="候选值"),
                ),
                ("field_sql", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "field_tips",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="提示文字"
                    ),
                ),
                ("field_rule", models.IntegerField(default=0, verbose_name="验证规则")),
                ("field_radio", models.IntegerField(default=0, verbose_name="排列方式")),
                ("field_editor", models.IntegerField(default=0, verbose_name="编辑器模式")),
                ("field_group", models.IntegerField(default=0, verbose_name="表单分组")),
                ("field_filter", models.IntegerField(default=0, verbose_name="作为筛选字段")),
                ("field_table", models.CharField(blank=True, max_length=50, null=True)),
                ("field_join", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "field_where",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "field_order",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("field_value", models.CharField(blank=True, max_length=50, null=True)),
                ("field_label", models.CharField(blank=True, max_length=50, null=True)),
                ("ordnum", models.IntegerField(default=0, verbose_name="字段排序")),
                ("islock", models.IntegerField(default=0, verbose_name="状态")),
                ("issys", models.IntegerField(default=0, verbose_name="类型转换")),
                ("isbase", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="ModelModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="模型名称")),
                ("tablename", models.CharField(max_length=50, verbose_name="模型标识")),
                (
                    "model_desc",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="模型描述"
                    ),
                ),
                (
                    "list_skins",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="列表模板"
                    ),
                ),
                (
                    "show_skins",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="内容模板"
                    ),
                ),
                (
                    "form_group",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="表单分组"
                    ),
                ),
                ("ordnum", models.IntegerField(default=0, verbose_name="模型排序")),
                ("islock", models.IntegerField(default=0, verbose_name="状态")),
                ("issys", models.IntegerField(default=0)),
                (
                    "leverstate",
                    models.SmallIntegerField(default=0, verbose_name="阅读权限"),
                ),
                ("buystate", models.SmallIntegerField(default=0, verbose_name="收费阅读")),
            ],
        ),
    ]