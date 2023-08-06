"use strict";

/**
 * Displays a thumbnail for a screenshot.
 *
 * Screenshot thumbnails allow the caption to be edited and the screenshot
 * to be deleted.
 *
 * This expects to take an existing element for the thumbnail contents, and
 * will attach handlers for interaction.
 *
 * The following signals are provided, on top of the standard Backbone.View
 * signals:
 *
 *     * beginEdit
 *       - Editing of the screenshot (caption) has begun.
 *
 *     * endEdit
 *       - Editing of the screenshot (caption) has finished.
 */
RB.ScreenshotThumbnail = Backbone.View.extend({
  events: {
    'click a.delete': '_onDeleteClicked'
  },

  /**
   * Render the thumbnail.
   *
   * This will listen for events on the screenshot and for events on the
   * thumbnail itself (to allow for caption editing).
   *
   * Returns:
   *     RB.ScreenshotThumbnail:
   *     This object, for chaining.
   */
  render: function render() {
    var _this = this;

    this.listenTo(this.model, 'destroy', function () {
      _this.$el.fadeOut(function () {
        return _this.remove();
      });
    });
    this.$caption = this.$el.find('a.edit').inlineEditor({
      editIconClass: 'rb-icon rb-icon-edit',
      showButtons: false
    }).on({
      'beginEdit': function beginEdit() {
        return _this.trigger('beginEdit');
      },
      'cancel': function cancel() {
        return _this.trigger('endEdit');
      },
      'complete': function complete(e, value) {
        /*
         * We want to set the caption after ready() finishes,
         * it case it loads state and overwrites.
         */
        _this.model.ready({
          ready: function ready() {
            _this.model.set('caption', value);

            _this.trigger('endEdit');

            _this.model.save();
          }
        });
      }
    });
    return this;
  },

  /**
   * Delete the screenshot.
   *
   * Once the screenshot has been deleted, the view will be removed.
   *
   * Args:
   *     e (Event):
   *         The event that triggered the delete.
   */
  _onDeleteClicked: function _onDeleteClicked(e) {
    e.preventDefault();
    e.stopPropagation();
    this.model.destroy();
  }
});

//# sourceMappingURL=screenshotThumbnailView.js.map