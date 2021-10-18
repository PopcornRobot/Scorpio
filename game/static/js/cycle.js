/**
 * @file Cycle - a dependency free javascript plugin for cycling through images
 *
 * @version 0.0.3
 * @author Brian Ruddy <briancruddy at gmail dot com>
 * @copyright 2015
 * @license MIT
 *
 */

var Cycle = (function () {
    
    'use strict';

    /**
     *
     * @type {{getDefaultOptions, initSettings, activateItem, removeClassFromElements, generateEmptyStyleSheet, getDataAttribute, toArray}}
     */
    var utils = (function () {
        
        return {

            /**
             * Get Cycle's default settings
             * @param {String} [option] - Retrieve a specific Cycle option
             * @returns {*}
             */
            getDefaultOptions: function (option) {
                var defaults = {
                    autoRun: true,
                    pauseOnHover: true,
                    selector: '.cycle',
                    target: 'li',
                    interval: '2500',
                    width: '300',
                    speed: '1000',
                    captionPosition: 'bottom',
                    captionColor: '#333',
                    captionBgColor: 'rgba(255, 255, 255, 0.75)'
                };

                return !option ? defaults : defaults[option];
            },

            /**
             * Get a Cycle instance's settings. Priority level: options object passed to constructor -> data-* attributes -> defaults
             * @param selector - CSS selector to get `data-*` attributes from the `Cycle.element`
             * @param [options] - An object containing Cycle settings
             * @returns {*}
             */
            initSettings: function (selector, options) {
                if (!options) options = {};

                var defaults = utils.getDefaultOptions();

                return {
                    autoRun: options.autoRun || defaults.autoRun,
                    pauseOnHover: options.pauseOnHover || defaults.pauseOnHover,
                    selector: selector || defaults.selector,
                    target: options.target || utils.getDataAttribute(selector, 'target') || defaults.target,
                    width: options.width || utils.getDataAttribute(selector, 'width') || defaults.width,
                    interval: options.interval || utils.getDataAttribute(selector, 'interval') || defaults.interval,
                    captionPosition: options.captionPosition || utils.getDataAttribute(selector, 'captionPosition') || defaults.captionPosition,
                    captionColor: options.captionColor || utils.getDataAttribute(selector, 'captionColor') || defaults.captionColor,
                    captionBgColor: options.captionBgColor || utils.getDataAttribute(selector, 'captionBg') || defaults.captionBgColor
                };

            },

            /**
             * Assigns `active` class to item
             * @param {NodeList} items - Collection of Cycle items
             * @param {Number} index - Index to select item from collection
             * @void
             */
            activateItem: function (items, index) {
                index %= items.length;
                items[index].classList.add('active');
            },

            /**
             * Remove `active` class from all cycle items
             * @param {NodeList} elements - Collection of DOMElements
             * @param {String} _class - Class to assign to `elements`
             * @void
             */
            removeClassFromElements: function (elements, _class) {
                for (var i = 0; i < elements.length; i++) {
                    elements[i].classList.remove(_class);
                }
            },

            /**
             * Generates an empty stylesheet and appends it to the document `<head>`
             * @returns {*}
             */
            generateEmptyStyleSheet: function () {
                var style = document.createElement('style');

                style.appendChild(document.createTextNode('')); // webkit hack
                document.head.appendChild(style);

                return style.sheet;
            },

            /**
             * Gets a DOM element based on the `selector` and returns the `data-*` attribute or an empty string
             * @param {String} selector - CSS selector to get `data-*` attributes from the `Cycle.element`
             * @param {String} attribute - `data-*` attribute name to retrieve
             * @returns {String}
             */
            getDataAttribute: function (selector, attribute) {
                var target = document.querySelector(selector);

                if (target.dataset.hasOwnProperty(attribute)) {
                    return target.dataset[attribute]
                }

                return '';
            },

            /**
             * Takes an array like object and returns the object in Array form
             * @param arrayLike - An array like object (IE `arguments`)
             * @returns {Array}
             */
            toArray: function (arrayLike) {
                var result = [];
                for (var i = 0; i < arrayLike.length; i++) {
                    result.push(arrayLike[i]);
                }

                return result;
            }
        };

    })();


    /**
     * @constructor
     * @param {String} [selector]
     * @param {Object} [options] - set options via arg object, data-* attrs, or just use the defaults
     * @property {Object} settings - object containing a Cycle instance's settings
     * @property {HTMLElement} element - parent element, `fire` and `on` both reference this element
     * @property {NodeList} items - collection containing items that cycle loops through
     * @property {NodeList} captions - collection containing captions
     * @property {Object} active - object containing the `index` of the current active item
     * @property {Boolean} continue - determines whether or not Cycle's `run` loop calls the `next` method
     * @returns {Cycle}
     */
    function Cycle(selector, options) {

        this.settings = utils.initSettings(selector, options);
        this.element = document.querySelector(this.settings.selector);
        this.items = utils.toArray(this.element.querySelectorAll(this.settings.target));
        this.captions = utils.toArray(this.element.querySelectorAll('.cycle-caption'));
        this.active = { index: 0 };
        this.continue = false;

        if (this.settings.autoRun) {
            this.style().run();
        }

        return this;
    }

    /**
     *
     * @type {{run: Function, delay: Function, pause: Function, resume: Function, next: Function, previous: Function, style: Function, fire: Function, on: Function, handleHover: Function}}
     */
    Cycle.prototype = {

        /**
         * Begins the cycle infinite loop
         * @chainable
         * @void
         */
        run: function () {
            this.fire('run', this);
            this.continue = true;
            this.handleHover();

            setInterval((function () {
                if (this.continue) {
                    this.next();
                }
            }).bind(this), this.settings.interval);

            return this;
        },

        /**
         * Delay Cycle's loop
         * @param {Number} timeout - Time in MS to delay Cycle
         * @param {Function} callback - Function to execute after delay
         * @chainable
         * @returns {Cycle}
         */
        delay: function (timeout, callback) {
            this.fire('delay', { instance: this, timeout: timeout });
            this.pause();

            setTimeout((function () {
                if (callback && typeof callback === 'function') {
                    callback();
                }
                this.resume();
            }).bind(this), timeout);

            return this;
        },

        /**
         * Pause Cycle's loop
         * @chainable
         * @returns {Cycle}
         */
        pause: function () {
            this.continue = false;
            this.fire('pause', this);

            return this;
        },

        /**
         * Resume Cycle's loop
         * @chainable
         * @returns {Cycle}
         */
        resume: function () {
            this.continue = true;
            this.fire('resume', this);

            return this;
        },

        /**
         * Render the next item in Cycle.items
         * @chainable
         * @returns {Cycle}
         */
        next: function () {
            utils.removeClassFromElements(this.items, 'active');

            this.active.index++;
            this.active.index %= this.items.length;
            utils.activateItem(this.items, this.active.index);

            this.fire('next', this);

            return this;
        },

        /**
         * Render the previous item in Cycle.items
         * @chainable
         * @returns {Cycle}
         */
        previous: function () {
            utils.removeClassFromElements(this.items, 'active');

            this.active.index--;
            if (this.active.index < 0)
                this.active.index = this.items.length - 1;

            utils.activateItem(this.items, this.active.index);

            this.fire('previous', this);

            return this;
        },

        /**
         * @param {Array} [customRules]
         * @chainable
         * @returns {Cycle}
         */
        style: function (customRules) {
            var styleSheet = utils.generateEmptyStyleSheet();

            var rules = [
                this.settings.selector + ' { max-width: 100%; position: relative; width: ' + this.settings.width + 'px; list-style: none; padding: 0; }',
                this.settings.selector + ' > ' + this.settings.target + ' { position: absolute; top: 0; left: 0; bottom: 0; right: 0; z-index: 0; opacity: 0; transition: opacity 300ms; }',
                this.settings.selector + ' > ' + this.settings.target + ':first-child { position: static; }',
                this.settings.selector + ' > .active { z-index: 1; opacity: 1; transition: opacity ' + this.settings.speed + 'ms; }',
                this.settings.selector + ' img { width: 100%; box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.4); }'
            ];

            if (this.captions.length > 0) {
                rules.push(this.settings.selector + ' .cycle-caption { position: absolute; left: 0; right: 0; padding: 5px 10px; ' + this.settings.captionPosition + ': 0; background-color: ' + this.settings.captionBgColor + '; color: ' + this.settings.captionColor + ' }');
            }


            rules.concat(customRules || []).forEach(function (rule) {
                styleSheet.insertRule(rule, 0);
            });

            return this;
        },

        /**
         * Fire a Cycle event on `Cycle.element`
         * @param {String} name - Event name, automatically prefixed with "cycle:"
         * @param {*} data - Passed as first argument to Cycle's `on` method's callback
         * @chainable
         * @returns {Cycle}
         */
        fire: function (name, data) {
            var event = new CustomEvent('cycle:' + name, {
                detail: {
                    settings: this,
                    data: data
                }
            });

            this.element.dispatchEvent(event);

            return this;
        },

        /**
         * Listen for events on `Cycle.element`
         * @param {String} eventType - Event name
         * @param {Function} callback - Function to be executed on event
         * @chainable
         * @returns {Cycle}
         */
        on: function (eventType, callback) {

            this.element.addEventListener(eventType, function (event) {
                var instanceData = event.detail.data;
                callback(instanceData, event);
            }, false);

            return this;
        },

        /**
         * Event listener for hover events on the Cycle object
         * @chainable
         * @returns {Cycle}
         */
        handleHover: function () {
            this.on('mouseenter', (function () {
                if (this.settings.pauseOnHover) {
                    this.pause();
                }
            }).bind(this));

            this.on('mouseout', (function () {
                if (this.settings.pauseOnHover) {
                    this.resume();
                }
            }).bind(this));

            return this;
        }
    };

    return Cycle;
})();