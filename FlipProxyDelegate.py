from PyQt5.QtSql import QSqlRelationalDelegate


class FlipProxyDelegate(QSqlRelationalDelegate):
    def createEditor(self, parent, option, index):
        proxy = index.model()
        base_index = proxy.mapToSource(index)
        return super(FlipProxyDelegate, self).createEditor(
            parent, option, base_index)

    def setEditorData(self, editor, index):
        proxy = index.model()
        base_index = proxy.mapToSource(index)
        return super(FlipProxyDelegate, self).setEditorData(editor, base_index)

    def setModelData(self, editor, model, index):
        base_model = model.sourceModel()
        base_index = model.mapToSource(index)
        return super(FlipProxyDelegate, self).setModelData(
            editor, base_model, base_index)