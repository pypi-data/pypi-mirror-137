"use strict";

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

suite('djblets/forms/views/ListEditView', function () {
  /*
   * See templates/djblets_forms/list_edit_widget.html.
   */
  var formTemplate = _.template("<div class=\"djblets-c-list-edit-widget\">\n <ul class=\"djblets-c-list-edit-widget__entries\">\n  <% if (items.length > 0) { %>\n   <% items.forEach(function(item, i) { %>\n    <li class=\"djblets-c-list-edit-widget__entry\"\n        data-list-index=\"<%- i %>\">\n     <input value=\"<%- item %>\" type=\"text\"<%= attrs %>>\n     <a href=\"#\" class=\"djblets-c-list-edit-widget__remove-item\"></a>\n    </li>\n   <% }); %>\n  <% } else { %>\n   <li class=\"djblets-c-list-edit-widget__entry\" data-list-index=\"0\">\n    <input type=\"text\">\n    <a href=\"#\" class=\"djblets-c-list-edit-widget__remove-item\"></a>\n   </li>\n  <% } %>\n </ul>\n <button class=\"djblets-c-list-edit-widget__add-item\"></button>\n <input class=\"djblets-c-list-edit-widget__value\"\n        type=\"hidden\" value=\"<%- nonZeroItems.join(',') %>\">\n</div>");

  var makeView = function makeView() {
    var items = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
    var attrs = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '';
    attrs = attrs.length ? " ".concat(attrs) : '';
    attrs = "".concat(attrs, " class=\"djblets-c-list-edit-widget__input\"");
    var $el = $(formTemplate({
      items: items,
      nonZeroItems: items.filter(function (i) {
        return i.length > 0;
      }),
      attrs: attrs
    })).appendTo($testsScratch);
    var view = new Djblets.Forms.ListEditView({
      el: $el,
      inputAttrs: attrs,
      sep: ','
    });
    view.render();
    return [view, view.$('.djblets-c-list-edit-widget__value')];
  };

  describe('Updating fields', function () {
    it('With no values', function () {
      var _makeView = makeView([]),
          _makeView2 = _slicedToArray(_makeView, 2),
          $valueField = _makeView2[1];

      expect($valueField.val()).toEqual('');
    });
    it('With one value', function () {
      var _makeView3 = makeView(['One']),
          _makeView4 = _slicedToArray(_makeView3, 2),
          view = _makeView4[0],
          $valueField = _makeView4[1];

      expect($valueField.val()).toEqual('One');
      view.$('.djblets-c-list-edit-widget__input').val('Foo').blur();
      expect($valueField.val()).toEqual('Foo');
    });
    it('With multiple values', function () {
      var _makeView5 = makeView(['one', 'two', 'three']),
          _makeView6 = _slicedToArray(_makeView5, 2),
          view = _makeView6[0],
          $valueField = _makeView6[1];

      var $inputs = view.$('.djblets-c-list-edit-widget__input');
      expect($valueField.val()).toEqual('one,two,three');
      $inputs.eq(2).val('baz').blur();
      expect($valueField.val()).toEqual('one,two,baz');
      $inputs.eq(0).val('').blur();
      expect($valueField.val()).toEqual('two,baz');
      $inputs.eq(1).val('').blur();
      expect($valueField.val()).toEqual('baz');
      $inputs.eq(2).val('').blur();
      expect($valueField.val()).toEqual('');
    });
  });
  describe('Removal', function () {
    it('With no values', function () {
      var _makeView7 = makeView([]),
          _makeView8 = _slicedToArray(_makeView7, 2),
          view = _makeView8[0],
          $valueField = _makeView8[1];

      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
    it('With one value', function () {
      var _makeView9 = makeView(['One']),
          _makeView10 = _slicedToArray(_makeView9, 2),
          view = _makeView10[0],
          $valueField = _makeView10[1];

      expect($valueField.val()).toEqual('One');
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
    it('With multiple values', function () {
      var _makeView11 = makeView(['One', 'Two', 'Three']),
          _makeView12 = _slicedToArray(_makeView11, 2),
          view = _makeView12[0],
          $valueField = _makeView12[1];

      expect($valueField.val()).toEqual('One,Two,Three');
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(3);
      view.$('.djblets-c-list-edit-widget__remove-item').eq(1).click();
      expect($valueField.val()).toEqual('One,Three');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(2);
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(2);
      view.$('.djblets-c-list-edit-widget__remove-item').eq(1).click();
      expect($valueField.val()).toEqual('One');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(1);
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
  });
  describe('Addition', function () {
    it('With values', function () {
      var _makeView13 = makeView(['one', 'two', 'three']),
          _makeView14 = _slicedToArray(_makeView13, 2),
          view = _makeView14[0],
          $valueField = _makeView14[1];

      expect($valueField.val()).toEqual('one,two,three');
      view.$('.djblets-c-list-edit-widget__add-item').click();
      expect($valueField.val()).toEqual('one,two,three');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(4);
      view.$('.djblets-c-list-edit-widget__input').eq(3).val('four').blur();
      expect($valueField.val()).toEqual('one,two,three,four');
    });
    it('With blank values', function () {
      var _makeView15 = makeView(['', '', '']),
          _makeView16 = _slicedToArray(_makeView15, 2),
          view = _makeView16[0],
          $valueField = _makeView16[1];

      expect($valueField.val()).toEqual('');
      view.$('.djblets-c-list-edit-widget__add-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(4);
      view.$('.djblets-c-list-edit-widget__input').eq(3).val('four').blur();
      expect($valueField.val()).toEqual('four');
    });
    it('With correct attributes', function () {
      var _makeView17 = makeView([], 'size="100" readonly'),
          _makeView18 = _slicedToArray(_makeView17, 1),
          view = _makeView18[0];

      view.$('.djblets-c-list-edit-widget__add-item').click();
      var $input = view.$('input').eq(1);
      expect($input.attr('size')).toEqual('100');
      expect($input.prop('readonly')).toBe(true);
    });
  });
});

//# sourceMappingURL=listEditViewTests.js.map