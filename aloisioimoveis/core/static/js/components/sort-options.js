Vue.component('sort-options', {
    template: `<div class='pull-right pull-left-md'>
                    <span class="order-text">Ordenar por:</span>
                    <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {{ this.currentOption.label }} <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu">
                        <li v-for="(option, index) in options">
                            <a v-bind:href="getOptionLink(index)" v-on:click="setCurrentOption(index)">{{ option.label }}</a>
                        </li>
                    </ul>
                </div>`,
    props: ['selected', 'parameters'],
    data: function() {
        return {
            currentOption: {},
            options: [
                { label: 'Mais recentes primeiro', value: '' },
                { label: 'Preço menor para o maior', value: 'valorcresc' },
                { label: 'Preço maior para o menor', value: 'valordecresc' }
            ]
        }
    },
    methods: {
        setCurrentOption: function(index) {
            this.currentOption = this.options[index];
        },
        getOptionLink: function(index) {
            if (this.parameters) {
                return this.parameters + '&ordem=' + this.options[index].value;
            }
            return '?ordem=' + this.options[index].value;
        }
    },
    created: function() {
        var found = false;
        for (var i = 0; i < this.options.length; i++) {
            if (this.options[i].value === this.selected) {
                this.currentOption = this.options[i];
                found = true;
                break;
            }
        }
        if (!found) {
            this.currentOption = this.options[0];
        }
    }
});
