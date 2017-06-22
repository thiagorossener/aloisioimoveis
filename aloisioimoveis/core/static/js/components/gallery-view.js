Vue.component('gallery-view', {
    template: `<div class="row">
                    <div class="col-md-12 col-lg-10">
                        <div class="view">
                            <div id="gallery" class="carousel slide" data-ride="carousel" data-interval="false">

                                <ol class="carousel-indicators">
                                    <li data-target="#gallery" v-for="(num, index) in photosTotal" 
                                        v-bind:class="{ active: index === 0 }"
                                        v-bind:data-slide-to="index"></li>
                                </ol>

                                <div class="carousel-inner">
                                    <slot name="main-view"></slot>
                                </div>

                                <a class="left carousel-control" href="#gallery" data-slide="prev">
                                    <span class="glyphicon glyphicon-chevron-left"></span>
                                    <span class="sr-only">Próxima</span>
                                </a>
                                <a class="right carousel-control" href="#gallery" data-slide="next">
                                    <span class="glyphicon glyphicon-chevron-right"></span>
                                    <span class="sr-only">Anterior</span>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-2 visible-lg">
                        <div class="gallery-scroll list-group">
                            <a href="javascript:void(0);" class="list-group-item controller"
                                v-on:click="up" v-bind:class="{ disabled: startIndex === 0 }">
                                <i class="fa fa-angle-up"></i>
                            </a>

                            <div class="gallery-scroll-content">
                                <slot name="menu-view"></slot>
                            </div>

                            <a href="javascript:void(0)" class="list-group-item controller"
                                v-on:click="down" v-bind:class="{ disabled: startIndex >= photosTotal - totalToShow }">
                                <i class="fa fa-angle-down"></i>
                            </a>
                        </div>
                    </div>
                </div>`,
    props: {
        photosTotal: {
            type: Number,
            required: true
        }
    },
    data: function() {
        return {
            startIndex: 0,
            totalToShow: 3
        };
    },
    methods: {
        up: function() {
            if ((this.startIndex - 1) >= 0) {
                this.startIndex--;
                this.$bus.$emit('changerange', this.range(this.startIndex, this.totalToShow));
            }
        },
        down: function() {
            if ((this.startIndex + 1) <= this.photosTotal - this.totalToShow) {
                this.startIndex++;
                this.$bus.$emit('changerange', this.range(this.startIndex, this.totalToShow));
            }
        },
        range(start, count) {
            return Array.apply(0, new Array(count))
                .map(function (element, index) {
                    return index + start;
                });
        }
    },
    mounted: function() {
        this.$bus.$emit('changerange', this.range(this.startIndex, this.totalToShow));
    }
});

Vue.component('gallery-menu-item', {
    template: `<a href="javascript:void(0);" class="picture-thumbnail" data-target="#gallery"
                       :data-slide-to="index" v-show="show">
                       <slot></slot>
               </a>`,
    props: {
        index: {
            type: Number,
            required: true
        }
    },
    data: function() {
        return {
            range: []
        }
    },
    computed: {
        show: function() {
            return this.range.indexOf(this.index) > -1;
        }
    },
    mounted: function() {
        this.$bus.$on('changerange', function(range) {
            this.range = range;
        }.bind(this));
    }
});
