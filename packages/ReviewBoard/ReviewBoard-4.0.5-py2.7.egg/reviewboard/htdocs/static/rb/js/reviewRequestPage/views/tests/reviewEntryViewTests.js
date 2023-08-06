"use strict";

suite('rb/reviewRequestPage/views/ReviewEntryView', function () {
  var template = "<div class=\"review review-request-page-entry\">\n <div class=\"review-request-page-entry-contents\">\n  <div class=\"collapse-button\"></div>\n  <div class=\"banners\">\n   <input type=\"button\" value=\"Publish\" />\n   <input type=\"button\" value=\"Discard\" />\n  </div>\n  <div class=\"comment-section\" data-context-type=\"body_top\">\n   <a class=\"add_comment_link\"></a>\n   <ul class=\"reply-comments\">\n    <li class=\"draft\" data-comment-id=\"456\">\n     <pre class=\"reviewtext\"></pre>\n    </li>\n   </ul>\n  </div>\n  <div class=\"comment-section\" data-context-id=\"123\"\n       data-context-type=\"diff_comments\">\n   <a class=\"add_comment_link\"></a>\n   <ul class=\"reply-comments\"></ul>\n  </div>\n  <div class=\"comment-section\" data-context-type=\"body_bottom\">\n   <a class=\"add_comment_link\"></a>\n   <ul class=\"reply-comments\"></ul>\n  </div>\n </div>\n</div>";
  var view;
  var reviewView;
  var reviewReply;
  beforeEach(function () {
    var reviewRequest = new RB.ReviewRequest();
    var editor = new RB.ReviewRequestEditor({
      reviewRequest: reviewRequest
    });
    var review = reviewRequest.createReview({
      loaded: true,
      links: {
        replies: {
          href: '/api/review/123/replies/'
        }
      }
    });
    var model = new RB.ReviewRequestPage.ReviewEntry({
      review: review,
      reviewRequest: reviewRequest,
      reviewRequestEditor: editor
    });
    var $el = $(template).appendTo($testsScratch);
    reviewReply = review.createReply();
    view = new RB.ReviewRequestPage.ReviewEntryView({
      el: $el,
      model: model
    });
    view.render();
    reviewView = view._reviewView;
    /* Don't allow the draft banner to show. */

    spyOn(reviewView, '_showReplyDraftBanner');
    spyOn(reviewView, 'trigger').and.callThrough();

    reviewView._setupNewReply(reviewReply);
  });
  describe('Actions', function () {
    it('Toggle collapse', function () {
      var $box = view.$('.review-request-page-entry-contents');
      var $collapseButton = view.$('.collapse-button');
      $collapseButton.click();
      expect($box.hasClass('collapsed')).toBe(true);
      $collapseButton.click();
      expect($box.hasClass('collapsed')).toBe(false);
    });
  });
  describe('Draft banner', function () {
    describe('Visibility', function () {
      it('Shown on hasDraft', function () {
        var editor = reviewView._replyEditorViews[1].model;

        reviewView._showReplyDraftBanner.calls.reset();

        expect(editor.get('hasDraft')).toBe(false);
        expect(reviewView._showReplyDraftBanner).not.toHaveBeenCalled();
        editor.set('hasDraft', true);
        expect(reviewView._showReplyDraftBanner).toHaveBeenCalled();
      });
    });
  });
  describe('Methods', function () {
    it('collapse', function () {
      view.collapse();
      expect(view.$('.review-request-page-entry-contents').hasClass('collapsed')).toBe(true);
    });
    it('expand', function () {
      var $box = view.$('.review-request-page-entry-contents').addClass('collapsed');
      view.expand();
      expect($box.hasClass('collapsed')).toBe(false);
    });
    describe('getReviewReplyEditorView', function () {
      it('With body_top', function () {
        var editorView = view.getReviewReplyEditorView('body_top');
        expect(editorView).not.toBe(undefined);
        expect(editorView).toBe(reviewView._replyEditorViews[0]);
      });
      it('With body_bottom', function () {
        var editorView = view.getReviewReplyEditorView('body_bottom');
        expect(editorView).not.toBe(undefined);
        expect(editorView).toBe(reviewView._replyEditorViews[2]);
      });
      it('With comments', function () {
        var editorView = view.getReviewReplyEditorView('diff_comments', 123);
        expect(editorView).not.toBe(undefined);
        expect(editorView).toBe(reviewView._replyEditorViews[1]);
      });
    });
  });
});

//# sourceMappingURL=reviewEntryViewTests.js.map