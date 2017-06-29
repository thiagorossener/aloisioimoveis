Vue.component('home-search', {
	template: `<div id="search" class="search-box" v-cloak>
                    <form class="form-inline" v-on:submit.prevent>
                        <fieldset>
                            <div class="form-group">
                                <label for="finalidade">O que você precisa?</label><br>
                                <div id="finalidade" class="btn-group" role="group">
                                    <button type="button" class="btn btn-default btn-lg"
                                            v-bind:class="{ active: params.finalidade === 'alugar' }"
                                            v-on:click="params.finalidade = 'alugar'">Alugar</button>
                                    <button type="button" class="btn btn-default btn-lg"
                                            v-bind:class="{ active: params.finalidade === 'comprar' }"
                                            v-on:click="params.finalidade = 'comprar'">Comprar</button>
                                </div>
                            </div>
                            <div class="form-group search-group">
                                <label>Qual tipo?</label><br>
                                <div class="btn-group">
                                    <button id="btn-tipo-de-imovel" class="btn btn-default btn-lg dropdown-toggle"
                                            type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        {{ selectedTipoDeImovel.label }} <span class="caret"></span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li v-for="(tipoDeImovel, index) in tiposDeImovel">
                                            <a href="javascript:void(0);"
                                               v-on:click="selectTipoDeImovel(index)">{{ tipoDeImovel.label }}</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="form-group search-group">
                                <label>Onde?</label><br>
                                <div class="btn-group">
                                    <button id="btn-cidades" class="btn btn-default btn-lg dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        {{ selectedCidade.label }} <span class="caret"></span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li v-for="(cidade, index) in cidades">
                                            <a href="javascript:void(0);"
                                               v-on:click="selectCidade(index)">{{ cidade.label }}</a>
                                        </li>
                                    </ul>
                                </div>
                                <div class="btn-group">
                                    <button id="btn-bairros" class="btn btn-default btn-lg dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        {{ selectedBairro.label }} <span class="caret"></span>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-bairros">
                                        <li v-for="(bairro, index) in bairros">
                                            <a href="javascript:void(0);"
                                               v-on:click="selectBairro(index)">{{ bairro.label }}</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="pull-right search-button-group">
                                <a href="javascript:void(0);" v-if="!searchForFicha" v-on:click="searchForFicha = true">Buscar por ficha</a>
                                <input id="input-numero-da-ficha" 
                                    type="number" class="input-lg"
                                    placeholder="Nº da ficha"
                                    v-model="ficha"
                                    v-else />
                                <a v-bind:href="submitButtonLink" id="btn-search" class="btn btn-lg" type="button"><i class="fa fa-search"></i> &nbsp;Buscar</a>
                            </div>
                        </fieldset>
                    </form>
                </div>`,
	props: {
	    baseUrl: {
	        type: String,
            required: true
        },
		finalidade: {
			type: String,
			default: function() {
				return 'alugar';
			}
		},
		tipo: {
			type: String,
			default: function() {
				return 'casa';
			}
		},
		cidade: {
			type: Number,
			default: function() {
				return 0;
			}
		},
		bairro: {
			type: Number,
			default: function() {
				return 0;
			}
		}
	},
	data: function() {
		return {
			params: {
				finalidade: null,
				tipo: null,
				cidade: null,
				bairro: null
			},
	        tiposDeImovel: [
	            { label: 'Casa', value: 'casa'},
	            { label: 'Apartamento', value: 'apartamento'},
	            { label: 'Comercial', value: 'comercial'},
	            { label: 'Terreno', value: 'terreno'}
	        ],
	        cidades: [],
	        bairros: [],
	        selectedTipoDeImovel: {},
	        selectedCidade: {},
	        selectedBairro: {},
	        searchForFicha: false,
            ficha: ''
		};
	},
	computed: {
		submitButtonLink: function() {
            if (this.ficha !== '') {
                return this.baseUrl + '?ficha=' + this.ficha;
            }
            return this.baseUrl + '?'
					+ 'bairro=' + this.params.bairro
					+ '&cidade=' + this.params.cidade
					+ '&finalidade=' + this.params.finalidade
					+ '&tipo=' + this.params.tipo;
		}
	},
	methods: {
        selectTipoDeImovel: function(index) {
            this.params.tipo = this.tiposDeImovel[index].value;
        },
        selectCidade: function(index) {
            this.params.cidade = this.cidades[index].value;
        },
        selectBairro: function(index) {
            this.params.bairro = this.bairros[index].value;
        }
    },
    watch: {
    	'params.tipo': function(value) {
    		this.selectedTipoDeImovel = this.tiposDeImovel[0];
    		for (let i = 0; i < this.tiposDeImovel.length; i++) {
    			if (value === this.tiposDeImovel[i].value) {
    				this.selectedTipoDeImovel = this.tiposDeImovel[i];
    				break;
    			}
    		}
    	},
    	'params.cidade': function(value) {
    		this.selectedCidade = this.cidades[0];
    		for (let i = 0; i < this.cidades.length; i++) {
    			if (value === this.cidades[i].value) {
    				this.selectedCidade = this.cidades[i];
    				break;
    			}
    		}
    	},
    	'params.bairro': function(value) {
			this.selectedBairro = this.bairros[0];
    		for (let i = 0; i < this.bairros.length; i++) {
    			if (value === this.bairros[i].value) {
    				this.selectedBairro = this.bairros[i];
    				break;
    			}
    		}
    	},
        selectedCidade: function(value, oldValue) {
        	this.params.bairro = null;
            this.$http
                .get('api/locations/neighborhoods?city=' + value.value)
                .then(function (response) {
                    if (response.data) {
                        this.bairros = [];

                        // Build list
                        $.each(response.data, function(key, obj) {
                            this.bairros.push({ label: obj.name, value: obj.id });
                        }.bind(this));

                        // Sort list
                        this.bairros = [{ value: 0, label: 'Todos os bairros' }].concat(this.bairros.sort(function(a,b) {
                            return (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0);
                        }));

                        // If it has changed from a city to another city and it isn't the first time it loads,
                        // update the neighborhood to 'Todos', if not, get the neighborhood from url params
                        if (oldValue.value && oldValue.value !== value.value) {
                        	this.params.bairro = this.bairros[0].value;
                        } else {
                        	this.params.bairro = this.bairro;
                        }
                    }
                }.bind(this));
        }
    },
    created: function() {
    	this.params.finalidade = this.finalidade;
    	this.params.tipo = this.tipo;

        this.$http
                .get('api/locations/cities')
                .then(function (response) {
                    if (response.data) {
                        this.cidades = [];

                        // Build list
                        $.each(response.data, function(key, obj) {
                            this.cidades.push({ label: obj.name, value: obj.id });
                        }.bind(this));

                        // Sort list
                        this.cidades = [{ value: 0, label: 'Todos as cidades' }].concat(this.cidades.sort(function(a,b) {
                            return (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0);
                        }));

                        this.params.cidade = this.cidade;
                    }
                }.bind(this));
    }
});
