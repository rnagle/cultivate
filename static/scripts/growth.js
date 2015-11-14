// Based on the stem generator in Flash Math Creativity

"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var EventManager = (function () {
  function EventManager() {
    _classCallCheck(this, EventManager);

    this.eventLookup = {};
  }

  _createClass(EventManager, [{
    key: "off",
    value: function off(event, callback) {
      var listeners = this.eventLookup[event];
      if (event === "*") this.eventLookup = {};else if (!callback) this.eventLookup[event] = [];else _.remove(listeners, { callback: callback });
    }
  }, {
    key: "on",
    value: function on(event, callback, scope) {
      var listeners = this.eventLookup[event];
      if (!listeners) this.eventLookup[event] = listeners = [];
      listeners.push({ callback: callback, scope: scope });
      return function () {
        return _.remove(listeners, { callback: callback });
      };
    }
  }, {
    key: "once",
    value: function once(event, callback, scope) {
      var _this = this;

      var on = function on() {
        for (var _len = arguments.length, data = Array(_len), _key = 0; _key < _len; _key++) {
          data[_key] = arguments[_key];
        }

        _this.off(event, on);
        callback.apply(scope, data);
      };
      return this.on(event, on);
    }
  }, {
    key: "fire",
    value: function fire(event) {
      for (var _len2 = arguments.length, data = Array(_len2 > 1 ? _len2 - 1 : 0), _key2 = 1; _key2 < _len2; _key2++) {
        data[_key2 - 1] = arguments[_key2];
      }

      var listeners = this.eventLookup[event];
      if (!listeners) return;
      listeners.forEach(function (list) {
        try {
          return list.callback.apply(list.scope, data);
        } catch (e) {
          return _.isError(e) ? e : new Error(e);
        }
      });
    }
  }]);

  return EventManager;
})();

var events = new EventManager();

var ns = "http://www.w3.org/2000/svg";
var d = "M0,0 Q5,-5 10,0 5,5 0,0z";

var stems = $("#stems");
var leaves = $("#leaves");
var svg = $("svg");

var leafCount = 30;
var plants = 10;
var centerX = 275;
var offsetX = 175;

function generate() {

  leaves.empty();
  stems.empty();

  _.times(plants, createPlant);

  stems.children().each(function () {
    var _this2 = this;

    var tween = TweenMax.to(this, _.random(2, 4, true), {
      drawSVG: true,
      delay: _.random(2, true),
      onStart: function onStart() {
        return TweenLite.set(_this2, { opacity: 1 });
      },
      onUpdate: function onUpdate() {
        return events.fire(_this2.id, tween.progress());
      }
    });
  });
}

function createPlant() {

  var points = createPoints();
  var stem = createPath(stems);
  var length = points.length;
  var values = points.map(function (point) {
    return point.x + "," + point.y;
  });
  var height = points[length - 1].y;
  var id = _.uniqueId("grow");
  var coords = [];

  for (var i = 0; i < length; i++) {
    var point = points[i];
    coords.push(point.x, point.y);
  }

  TweenLite.set(stem, {
    opacity: 0,
    drawSVG: 0,
    //attr: { id, d: `M${values.join(" ")}` }
    attr: { id: id, d: solve(coords) }
  });

  for (var i = 0; i < leafCount; i++) {
    var point = points[length - 1 - i];
    var scale = {
      x: 1 + 0.1 * i,
      y: 1 + 0.05 * i
    };
    createLeaf(point, scale, height, id);
  }
}

function createLeaf(point, scale, height, grow) {

  var leaf = createPath(leaves);
  var start = height / point.y;
  var off = events.on(grow, growLeaf);

  function growLeaf(growth) {

    if (growth >= start) {

      // Remove listener
      off();

      TweenLite.set(leaf, {
        x: point.x,
        y: point.y,
        scaleX: scale.x,
        scaleY: scale.y,
        rotation: _.random(180) - 180,
        fill: "rgb(0," + _.random(110, 160) + ",0)",
        attr: { d: d }
      });

      TweenLite.from(leaf, 1, { scale: 0 });
    }
  }
}

function createPoints() {

  var x = _.random(centerX - offsetX, centerX + offsetX);
  var y = 400;
  var dy = 5;
  var offset = 0.007;
  var count = _.random(30, 55);
  var points = [{ x: x, y: y }];

  for (var i = 1; i <= count; i++) {
    points.push({
      x: points[i - 1].x + i * offset * (_.random(21) - 10),
      y: 395 - dy * i
    });
  }
  return points;
}

function createPath(parent) {
  return $(document.createElementNS(ns, "path")).appendTo(parent);
}

function solve(data) {

  var size = data.length;
  var last = size - 4;

  var path = "M" + [data[0], data[1]];

  for (var i = 0; i < size - 2; i += 2) {

    var x0 = i ? data[i - 2] : data[0];
    var y0 = i ? data[i - 1] : data[1];

    var x1 = data[i + 0];
    var y1 = data[i + 1];

    var x2 = data[i + 2];
    var y2 = data[i + 3];

    var x3 = i !== last ? data[i + 4] : x2;
    var y3 = i !== last ? data[i + 5] : y2;

    var cp1x = (-x0 + 6 * x1 + x2) / 6;
    var cp1y = (-y0 + 6 * y1 + y2) / 6;

    var cp2x = (x1 + 6 * x2 - x3) / 6;
    var cp2y = (y1 + 6 * y2 - y3) / 6;

    path += "C" + [cp1x, cp1y, cp2x, cp2y, x2, y2];
  }

  return path;
}