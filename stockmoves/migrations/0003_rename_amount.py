from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("stockmoves", "0002_priority_81")]

    operations = [
        migrations.RenameField(model_name="stockmove", old_name="amount_cents", new_name="amount"),
    ]
