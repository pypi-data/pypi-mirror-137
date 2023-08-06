"use strict";

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

(function () {
  var _Promise$withResolver = Promise.withResolver(),
      _Promise$withResolver2 = _slicedToArray(_Promise$withResolver, 2),
      readyPromise = _Promise$withResolver2[0],
      resolve = _Promise$withResolver2[1];
  /**
   * A form for managing the settings of avatar services.
   *
   * This form lets you select the avatar service you wish to use, as well as
   * configure the settings for that avatar service.
   */


  Djblets.Avatars.SettingsFormView = Backbone.View.extend({
    events: {
      'change #id_avatar_service_id': '_onServiceChanged',
      'submit': '_onSubmit'
    },

    /**
     * Initialize the form.
     */
    initialize: function initialize() {
      var _this = this;

      console.assert(Djblets.Avatars.SettingsFormView.instance === null);
      Djblets.Avatars.SettingsFormView.instance = this;
      this._configForms = new Map();
      this._$config = this.$('.avatar-service-configuration');
      var services = this.model.get('services');
      this.listenTo(this.model, 'change:serviceID', function () {
        return _this._showHideForms();
      });
      /*
       * The promise continuations will only be executed once the stack is
       * unwound.
       */

      resolve();
    },

    /**
     * Validate the current form upon submission.
     *
     * Args:
     *     e (Event):
     *         The form submission event.
     */
    _onSubmit: function _onSubmit(e) {
      var serviceID = this.model.get('serviceID');

      var currentForm = this._configForms.get(serviceID);

      if (currentForm && !currentForm.validate()) {
        e.preventDefault();
      }
    },

    /**
     * Render the child forms.
     *
     * This will show the for the currently selected service if it has one.
     *
     * Returns:
     *     Djblets.Avatars.SettingsFormView:
     *     This view (for chaining).
     */
    renderForms: function renderForms() {
      var _iterator = _createForOfIteratorHelper(this._configForms.values()),
          _step;

      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var form = _step.value;
          form.render();
        }
        /*
         * Ensure that if the browser sets the value of the <select> upon
         * refresh that we update the model accordingly.
         */

      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }

      this.$('#id_avatar_service_id').change();

      this._showHideForms(true);

      return this;
    },

    /**
     * Show or hide the configuration form.
     */
    _showHideForms: function _showHideForms() {
      var services = this.model.get('services');
      var serviceID = this.model.get('serviceID');

      var currentForm = this._configForms.get(serviceID);

      var previousID = this.model.previous('serviceID');
      var previousForm = previousID ? this._configForms.get(previousID) : undefined;

      if (previousForm && currentForm) {
        previousForm.$el.hide();
        currentForm.$el.show();
      } else if (previousForm) {
        previousForm.$el.hide();

        this._$config.hide();
      } else if (currentForm) {
        currentForm.$el.show();

        this._$config.show();
      }
    },

    /**
     * Handle the service being changed.
     *
     * Args:
     *     e (Event):
     *         The change event.
     */
    _onServiceChanged: function _onServiceChanged(e) {
      var $target = $(e.target);
      this.model.set('serviceID', $target.val());
    }
  }, {
    /**
     * The form instance.
     */
    instance: null,

    /**
     * Add a configuration form to the instance.
     *
     * Args:
     *     serviceID (string):
     *         The unique ID for the avatar service.
     *
     *     formClass (constructor):
     *         The view to use for the form.
     */
    addConfigForm: function addConfigForm(serviceID, formClass) {
      Djblets.Avatars.SettingsFormView.instance._configForms.set(serviceID, new formClass({
        el: $("[data-avatar-service-id=\"".concat(serviceID, "\"]")),
        model: Djblets.Avatars.SettingsFormView.instance.model
      }));
    },

    /**
     * A promise that is resolved when the avatar services form has been
     * initialized.
     */
    ready: readyPromise
  });
})();

//# sourceMappingURL=avatarSettingsFormView.js.map