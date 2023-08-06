"use strict";

/**
 * Display a list item for a config page.
 *
 * The list item will show information on the item and any actions that can
 * be invoked.
 *
 * By default, this will show the text from the ListItem model, linking it
 * if the model has an editURL attribute. This can be customized by subclasses
 * by overriding `template`.
 */
Djblets.Config.ListItemView = Backbone.View.extend({
  tagName: 'li',
  className: 'djblets-c-config-forms-list__item',
  iconBaseClassName: 'djblets-icon',

  /**
   * A mapping of item states to CSS classes.
   *
   * Subclasses can extend this to provide custom CSS classes, or support
   * custom item states.
   */
  itemStateClasses: {
    disabled: '-is-disabled',
    enabled: '-is-enabled',
    error: '-has-error'
  },
  actionHandlers: {},
  template: _.template("<% if (editURL) { %>\n<a href=\"<%- editURL %>\"><%- text %></a>\n<% } else { %>\n<%- text %>\n<% } %>"),

  /**
   * Initialize the view.
   */
  initialize: function initialize() {
    this.listenTo(this.model, 'actionsChanged', this.render);
    this.listenTo(this.model, 'request', this.showSpinner);
    this.listenTo(this.model, 'sync', this.hideSpinner);
    this.listenTo(this.model, 'destroy', this.remove);
    this.$spinnerParent = null;
    this.$spinner = null;
  },

  /**
   * Render the view.
   *
   * This will be called every time the list of actions change for
   * the item.
   *
   * Returns:
   *     Djblets.Config.ListItemView:
   *     This view.
   */
  render: function render() {
    var model = this.model;
    this.$el.empty().append(this.template(_.defaults(model.attributes, this.getRenderContext())));
    this._$itemState = this.$('.djblets-c-config-forms-list__item-state');
    this.listenTo(model, 'change:itemState', this._onItemStateChanged);

    this._onItemStateChanged();

    this.addActions(this.getActionsParent());
    return this;
  },

  /**
   * Return additional render context.
   *
   * By default this returns an empty object. Subclasses can use this to
   * provide additional values to :js:attr:`template` when it is rendered.
   *
   * Returns:
   *     object:
   *     Additional rendering context for the template.
   */
  getRenderContext: function getRenderContext() {
    return {};
  },

  /**
   * Remove the item.
   *
   * This will fade out the item, and then remove it from view.
   */
  remove: function remove() {
    var _this = this;

    this.$el.fadeOut('normal', function () {
      return Backbone.View.prototype.remove.call(_this);
    });
  },

  /**
   * Return the container for the actions.
   *
   * This defaults to being this element, but it can be overridden to
   * return a more specific element.
   *
   * Returns:
   *     jQuery:
   *     The container for the actions.
   */
  getActionsParent: function getActionsParent() {
    return this.$el;
  },

  /**
   * Display a spinner on the item.
   *
   * This can be used to show that the item is being loaded from the
   * server.
   */
  showSpinner: function showSpinner() {
    if (this.$spinner) {
      return;
    }

    this.$el.attr('aria-busy', 'true');
    this.$spinner = $('<span>').addClass('djblets-o-spinner').attr('aria-hidden', 'true').prependTo(this.$spinnerParent).hide().css('visibility', 'visible').fadeIn();
  },

  /**
   * Hide the currently visible spinner.
   */
  hideSpinner: function hideSpinner() {
    var _this2 = this;

    if (!this.$spinner) {
      return;
    }
    /*
     * The slow fadeout does two things:
     *
     * 1) It prevents the spinner from disappearing too quickly
     *    (in combination with the fadeIn above), in case the operation
     *    is really fast, giving some feedback that something actually
     *    happened.
     *
     * 2) By fading out, it doesn't look like it just simply stops.
     *    Helps provide a sense of completion.
     */


    this.$spinner.fadeOut('slow', function () {
      _this2.$spinner.remove();

      _this2.$spinner = null;
    });
    this.$el.removeAttr('aria-busy');
  },

  /**
   * Add all registered actions to the view.
   *
   * Args:
   *     $parentEl (jQuery):
   *         The parent element to add the actions to.
   */
  addActions: function addActions($parentEl) {
    var _this3 = this;

    var $actions = $('<span>').addClass('djblets-c-config-forms-list__item-actions');
    this.model.actions.forEach(function (action) {
      var $action = _this3._buildActionEl(action).appendTo($actions);

      if (action.children) {
        if (action.label) {
          $action.append(' &#9662;');
        }
        /*
         * Show the dropdown after we let this event propagate.
         */


        $action.click(function () {
          return _.defer(function () {
            return _this3._showActionDropdown(action, $action);
          });
        });
      }
    });
    this.$spinnerParent = $actions;
    $actions.prependTo($parentEl);
  },

  /**
   * Show a dropdown for a menu action.
   *
   * Args:
   *     action (object):
   *         The action to show the dropdown for. See
   *         :js:class:`Djblets.Config.ListItem`. for a list of attributes.
   *
   *     $action (jQuery):
   *         The element that represents the action.
   */
  _showActionDropdown: function _showActionDropdown(action, $action) {
    var _this4 = this;

    var actionPos = $action.position();
    var $menu = $('<div/>').css({
      minWidth: $action.outerWidth(),
      position: 'absolute'
    }).addClass('djblets-c-config-forms-popup-menu').click(function (e) {
      return e.stopPropagation();
    });
    var $items = $('<ul/>').addClass('djblets-c-config-forms-popup-menu__items').appendTo($menu);
    var actionLeft = actionPos.left + $action.getExtents('m', 'l');
    action.children.forEach(function (childAction) {
      return $('<li/>').addClass('djblets-c-config-forms-popup-menu__item ' + "config-forms-list-action-row-".concat(childAction.id)).append(_this4._buildActionEl(childAction)).appendTo($items);
    });
    this.trigger('actionMenuPopUp', {
      action: action,
      $action: $action,
      $menu: $menu
    });
    $menu.appendTo($action.parent());
    var winWidth = $(window).width();
    var paneWidth = $menu.width();
    $menu.move($action.offset().left + paneWidth > winWidth ? actionLeft + $action.innerWidth() - paneWidth : actionLeft, actionPos.top + $action.outerHeight(), 'absolute');
    /* Any click outside this dropdown should close it. */

    $(document).one('click', function () {
      _this4.trigger('actionMenuPopDown', {
        action: action,
        $action: $action,
        $menu: $menu
      });

      $menu.remove();
    });
  },

  /**
   * Build the element for an action.
   *
   * If the action's type is ``'checkbox'``, a checkbox will be shown.
   * Otherwise, the action will be shown as a button.
   *
   * Args:
   *     action (object):
   *         The action to show the dropdown for. See
   *         :js:class:`Djblets.Config.ListItem` for a list of attributes.
   */
  _buildActionEl: function _buildActionEl(action) {
    var _this5 = this;

    var enabled = action.enabled !== false;
    var actionHandlerName = enabled ? this.actionHandlers[action.id] : null;
    var isCheckbox = action.type === 'checkbox';
    var isRadio = action.type === 'radio';
    var $action;
    var $result;

    if (isCheckbox || isRadio) {
      var inputID = _.uniqueId('action_' + action.type);

      $action = $('<input/>').attr({
        name: action.name,
        type: action.type,
        id: inputID
      });
      var $label = $('<label>').attr('for', inputID).text(action.label);

      if (action.id) {
        $label.addClass("config-forms-list-action-label-".concat(action.id));
      }

      $result = $('<span/>').append($action).append($label);

      if (action.propName) {
        if (isCheckbox) {
          $action.bindProperty('checked', this.model, action.propName);
        } else if (isRadio) {
          $action.bindProperty('checked', this.model, action.propName, {
            radioValue: action.radioValue
          });
        }
      }

      if (action.enabledPropName) {
        $action.bindProperty('disabled', this.model, action.enabledPropName, {
          inverse: action.enabledPropInverse !== true
        });
      }

      if (actionHandlerName) {
        var actionHandler = _.debounce(_.bind(this[actionHandlerName], this), 50, true);

        $action.change(actionHandler);

        if (isRadio && action.dispatchOnClick) {
          $action.click(actionHandler);
        }
      }
    } else {
      if (action.url) {
        $action = $('<a class="btn" role="button">').attr('href', action.url);
      } else {
        $action = $('<button type="button">');
      }

      $result = $action;

      if (action.label) {
        $action.text(action.label);
      }

      if (action.ariaLabel) {
        $action.attr('aria-label', action.ariaLabel);
      }

      if (action.iconName) {
        $action.prepend($('<span>').addClass(this.iconBaseClassName).addClass("".concat(this.iconBaseClassName, "-").concat(action.iconName)));
      }

      if (actionHandlerName) {
        $action.click(function (evt) {
          evt.preventDefault();
          evt.stopPropagation();

          _this5._onActionButtonClicked(evt, actionHandlerName, $action);
        });
      }
    }

    $action.addClass('djblets-c-config-forms-list__item-action');

    if (action.id) {
      $action.addClass("config-forms-list-action-".concat(action.id));
    }

    if (action.danger) {
      $action.addClass('-is-danger');
    }

    if (action.primary) {
      $action.addClass('-is-primary');
    }

    if (!enabled) {
      $action.prop('disabled', true);
    }

    return $result;
  },

  /**
   * Handle changes to the item state.
   *
   * This will update the CSS class used on the item and any relevant text
   * contained within the item to reflect the current state.
   */
  _onItemStateChanged: function _onItemStateChanged() {
    var model = this.model;
    var oldItemState = model.previous('itemState');
    var itemState = model.get('itemState');

    if (oldItemState) {
      this.$el.removeClass(this.itemStateClasses[oldItemState]);
    }

    if (itemState) {
      this.$el.addClass(this.itemStateClasses[itemState]);
      /*
       * Note that if we didn't find an element in the template for
       * this before, this is basically a no-op.
       */

      this._$itemState.text(model.itemStateTexts[itemState]);
    }
  },

  /**
   * Handle clicks on a list item action button.
   *
   * This will invoke the click handler on the view. If that handler
   * returns a Promise, this will disable the button, replace its contents
   * with a spinner, and then wait for the promise to resolve before
   * setting the button's contents and enabled states back to normal.
   *
   * Args:
   *     evt (jQuery.Event):
   *         The click event on the button.
   *
   *     actionHandlerName (string):
   *         The name of the action handler function to call.
   *
   *     $action (jQuery):
   *         The action button that was clicked.
   */
  _onActionButtonClicked: function _onActionButtonClicked(evt, actionHandlerName, $action) {
    var promise = this[actionHandlerName].call(this, evt);

    if (promise && typeof promise.then === 'function') {
      $action.prop('disabled', true);
      var childrenHTML = $action.html();
      $action.empty();
      var $spinner = $('<span class="djblets-o-spinner">').appendTo($action);
      /*
       * This is a promise, so there's an async operation
       * going on. Set up the spinner.
       */

      promise.finally(function () {
        $spinner.remove();
        $action.html(childrenHTML);
        $action.prop('disabled', false);
      });
    }
  }
});

//# sourceMappingURL=listItemView.js.map