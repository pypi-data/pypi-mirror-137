"use strict";

suite('djblets/configForms/views/TableItemView', function () {
  describe('Rendering', function () {
    describe('Item display', function () {
      it('With editURL', function () {
        var item = new Djblets.Config.ListItem({
          editURL: 'http://example.com/',
          text: 'Label'
        });
        var itemView = new Djblets.Config.TableItemView({
          model: item
        });
        itemView.render();
        expect(itemView.$el.html().strip()).toBe(['<td>', '<span class="djblets-c-config-forms-list__item-actions">', '</span>\n\n', '<a href="http://example.com/">Label</a>\n\n', '</td>'].join(''));
      });
      it('Without editURL', function () {
        var item = new Djblets.Config.ListItem({
          text: 'Label'
        });
        var itemView = new Djblets.Config.TableItemView({
          model: item
        });
        itemView.render();
        expect(itemView.$el.html().strip()).toBe(['<td>', '<span class="djblets-c-config-forms-list__item-actions">', '</span>\n\n', 'Label\n\n', '</td>'].join(''));
      });
    });
    describe('Action placement', function () {
      it('Default template', function () {
        var item = new Djblets.Config.ListItem({
          text: 'Label',
          actions: [{
            id: 'mybutton',
            label: 'Button'
          }]
        });
        var itemView = new Djblets.Config.TableItemView({
          model: item
        });
        itemView.render();
        var $button = itemView.$('td:last button.djblets-c-config-forms-list__item-action');
        expect($button.length).toBe(1);
        expect($button.text()).toBe('Button');
      });
      it('Custom template', function () {
        var CustomTableItemView = Djblets.Config.TableItemView.extend({
          template: _.template("<td></td>\n<td></td>")
        });
        var item = new Djblets.Config.ListItem({
          text: 'Label',
          actions: [{
            id: 'mybutton',
            label: 'Button'
          }]
        });
        var itemView = new CustomTableItemView({
          model: item
        });
        itemView.render();
        var $button = itemView.$('td:last button.djblets-c-config-forms-list__item-action');
        expect($button.length).toBe(1);
        expect($button.text()).toBe('Button');
      });
    });
  });
});

//# sourceMappingURL=tableItemViewTests.js.map