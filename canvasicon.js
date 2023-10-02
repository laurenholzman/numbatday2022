(function (factory, window) {
    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['leaflet'], function (L) {
            return factory(L);
        });
    } else if (typeof module !== 'undefined') {
        // Node/CommonJS
        module.exports = factory(require('leaflet'));
    } else {
        // Browser global
        if (typeof window.L === 'undefined') {
            throw new Error('Leaflet must be loaded first');
        }
        window.L.CanvasIcon = factory(window.L);
    }
}(function (L) {
    'use strict';

    /**
     * Canvas Icon
     * @type {L.CanvasIcon}
     * @extends {L.Icon}
     */
    L.CanvasIcon = L.Icon.extend({
        options: {
            iconSize: [24, 24],
            iconAnchor: [12, 12],
            drawIcon: null,
            className: 'leaflet-canvas-icon'
        },

        createIcon: function (oldIcon) {
            var div = oldIcon || document.createElement('div');
            div.innerHTML = '<canvas></canvas>';
            var canvas = div.querySelector('canvas');

            var size = L.point(this.options.iconSize);
            canvas.width = size.x;
            canvas.height = size.y;

            this._setIconStyles(canvas, 'icon');

            if (typeof this.options.drawIcon === 'function') {
                this.options.drawIcon.call(this, canvas);
            }

            return div;
        },

        createShadow: function () {
            return null;
        },

        _setIconStyles: function (img, name) {
            if (typeof this.options.drawIcon === 'function') {
                this.options.drawIcon.call(this, img);
            }

            L.Icon.prototype._setIconStyles.call(this, img, name);
        }
    });

    /**
     * Canvas Icon factory
     * @param {Object} options
     * @returns {L.CanvasIcon}
     */
    L.canvasIcon = function (options) {
        return new L.CanvasIcon(options);
    };

    return L.CanvasIcon;
}, window));
