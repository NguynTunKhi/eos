(function($){
    
    /**
     * Get class-like object
     * @param {Object} data
     * @returns {Function}
     */
    $.Class = function(data){
        var Constructor, my = {};

        // collection of dependencies
        my._extends = [];

        // function to return
        Constructor = function(){
            var self = this;

            // bind function to this
            this.delegate(/^_/);

            // call constructors in extends
            $.each(this.__extends__, function(i, o){
                if($.isFunction(o._initialize)){
                    o._initialize.call(self);
                }
            });

            // define element
            if(!! this.el){
                this.$el = $(this.el);
            }

            // call constructor
            if("function" === $.type(this._initialize)){
                this._initialize.apply(this, arguments);
            }
        };

        // append object to `extends` recursively
        my.append = function(items){
            if("array" !== $.type(items)){ return; }
            $.each(items, function(i, item){
                var obj = null;
                switch($.type(item)){
                    case "string": obj = $.Class.modules[item]; break;
                    case "function": obj = item.prototype; break;
                    case "object": obj = item; break;
                    default: break;
                }
                if(! obj){ return; }
                my.append(obj._extends);
                my._extends.push(obj);
            });
        };

        // resolve dependencies, set as prop
        my.append(data._extends);
        data.__extends__ = my._extends;

        // merge all
        my.args = [true, Constructor.prototype, $.Class.modules.common];
        $.extend.apply($, my.args.concat(my._extends).concat([data]));

        return Constructor;
    };

    /**
     * Prototypes with features
     * Initialize feature by `_initialize` function in constructor
     */
    var modules = $.Class.modules = {};

    /**
     * Common
     * - Initialize dependencies
     * - Initialize element with `el`
     */
    modules.common = {
        el: null,
        $el: null,
        _extends: [],

        /**
         * Bind function to `this`
         * @param {String|Array|Regexp} name
         * @param {Object} obj (optional)
         */
        delegate: function(name, obj){
            var type, process;
            
            obj = obj || this;
            type = $.type(name);
            process = function(i, name){
                if(! $.isFunction(obj[name])){ return; }
                obj[name] = $.proxy(obj[name], obj);
            };
            if(type === "regexp"){
                $.each(obj, function(key, value){
                    if(! name.test(key)){ return; }
                    process(null, key);
                });
                return this;
            }
            name = (type !== "array") ? [name] : name;
            $.each(name, process);
            return this;
        }
    };

    /**
     * Events
     * - Extend jQuery's event feature (on, off, trigger)
     */
    modules.events = {
        _initialize: function(){
            var jq, my = this;
            jq = $(this);
            $.each(["on", "off", "trigger"], function(i, name){
                my[name] = $.proxy(jq[name], jq);
            });
        }
    };

    /**
     * Config
     * - Configure values in `options` prop
     */
    modules.config = {
        _options: null,
        options: null,

        _initialize: function(){
            this.options = {};
            this.config(this._options);
        },

        /**
         * Set/get values of options
         *
         * - .config(key, value); // set value
         * - .config(key); // returns value
         * - .config(obj); // set values
         * - .config(); // returns values
         */
        config: function(){
            var args = Array.prototype.slice.call(arguments);
            switch($.type(args[0])){
                case "undefined":
                    return this.options;
                case "string": 
                    if(args.length > 1){
                        this.options[args[0]] = args[1];
                        return this;
                    }
                    return this.options[args[0]];
                case "object":
                    $.extend(true, this.options, args[0]);
                    return this;
                default: break;
            }
            return this;
        }
    };

    /**
     * Attributes
     * - Configure values in `attributes` prop
     * - If extended with `events`, 'change' event triggered when a value changed
     */
    modules.attributes = {
        EVENT_CHANGE: "change",

        _attributes: null,
        attributes: null,

        _initialize: function(){
            this.attributes = {};
            this.attr(this._attributes);
        },

        /**
         * Set/get values of options
         *
         * - .attr(key, value); // set value
         * - .attr(key); // returns value
         * - .attr(obj); // set values
         * - .attr(); // returns values
         */
        attr: function(){
            var my = this,
                args = Array.prototype.slice.call(arguments),
                changed = false;
            switch($.type(args[0])){
                case "undefined":
                    return this.attributes;
                case "string": 
                    if(args.length > 1){
                        changed = this.attributes[args[0]] !== args[1];
                        this.attributes[args[0]] = args[1];
                        if(changed && $.isFunction(this.trigger)){
                            this.trigger(this.EVENT_CHANGE, {key: args[0], value: args[1]});
                        }
                        return this;
                    }
                    return this.attributes[args[0]];
                case "object":
                    $.each(args[0], function(key, value){
                        my.attr(key, value);
                    });
                    return this;
                default: break;
            }
            return this;
        }
    };

    /**
     * Manupulate module container
     */
    $.Class.classes = {};
    $.Class.instances = {};

    /**
     * Exports class by name
     * @param {String} name
     * @param {Object} data
     * @param {Boolean} force (optional)
     */
    $.Class.exports = function(name, data, force){
        var modules = $.Class.modules;
        if((name in modules) && !force){
            throw new Error("module named '%%' is already exists.".replace("%%", name));
        }
        modules[name] = data;
        return this;
    };


    /**
     * Require class instance by name
     * @param {String} name
     * @param {Boolean} force
     */
    $.Class.require = function(name, force){
        var modules, instances, feature;

        modules = $.Class.modules;
        instances = $.Class.instances;
        feature = $.Class.find(name);

        switch(true){
            case force:
                if(feature){
                    return new feature();
                }
                break;
            case name in instances:
                return instances[name];
            case name in modules:
                instances[name] = new feature();
                return instances[name];
            default: break;
        }

        return null;
    };

    /**
     * Find module by name
     */
    $.Class.find = function(name){
        var classes, modules;

        classes = $.Class.classes;
        modules = $.Class.modules;

        if(! (name in classes) && (name in modules)){
            classes[name] = $.Class(modules[name]);
        }

        return classes[name];
    };

    /**
     * Exports
     */
    $.exports = $.Class.exports;
    $.require = $.Class.require;

}(jQuery));
