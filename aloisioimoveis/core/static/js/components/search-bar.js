Vue.component('search-bar', {
	template: `
	<section class="top-page">
	    <div class="container">
	        <div id="search" class="search-box" v-cloak>
	            <form class="form-inline">
	                <fieldset>
	                    <div class="form-group">
	                        <label for="finalidade">O que você precisa?</label><br>
	                        <div id="finalidade" class="btn-group" role="group">
	                            <button type="button" class="btn btn-default"
	                                    v-bind:class="{ active: params.finalidade === 'alugar' }"
	                                    v-on:click="params.finalidade = 'alugar'">Alugar</button>
	                            <button type="button" class="btn btn-default"
	                                    v-bind:class="{ active: params.finalidade === 'comprar' }"
	                                    v-on:click="params.finalidade = 'comprar'">Comprar</button>
	                        </div>
	                    </div>
	                    <div class="form-group search-group">
	                        <label>Qual tipo?</label><br>
	                        <div class="btn-group">
	                            <button id="btn-tipo-de-imovel" class="btn btn-default dropdown-toggle"
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
	                            <button id="btn-cidades" class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
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
	                            <button id="btn-bairros" class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
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
	                    <div class="form-group">
	                        <a v-bind:href="submitButtonLink" id="btn-search" class="btn" type="button"><i class="fa fa-search"></i> &nbsp;Buscar</a>
	                    </div>
	                </fieldset>
	            </form>
	        </div>
	    </div>
	</section>`,
	props: {
		finalidade: {
			type: String,
			default: function() {
				return 'alugar';
			}
		},
		tipo: {
			type: String,
			default: function() {
				return '';
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
	        selectedBairro: {}
		};
	},
	computed: {
		submitButtonLink: function() {
			return 'busca.php?finalidade=' + this.params.finalidade
				   + '&tipo=' + this.params.tipo
				   + '&cidade=' + this.params.cidade
				   + '&bairro=' + this.params.bairro;
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
    		for (var i = 0; i < this.tiposDeImovel.length; i++) {
    			if (value === this.tiposDeImovel[i].value) {
    				this.selectedTipoDeImovel = this.tiposDeImovel[i];
    				break;
    			}
    		}
    	},
    	'params.cidade': function(value) {
    		this.selectedCidade = this.cidades[0];
    		for (var i = 0; i < this.cidades.length; i++) {
    			if (value === this.cidades[i].value) {
    				this.selectedCidade = this.cidades[i];
    				break;
    			}
    		}
    	},
    	'params.bairro': function(value) {
			this.selectedBairro = this.bairros[0];
    		for (var i = 0; i < this.bairros.length; i++) {
    			if (value === this.bairros[i].value) {
    				this.selectedBairro = this.bairros[i];
    				break;
    			}
    		}
    	},
        selectedCidade: function(value, oldValue) {
        	this.params.bairro = null;
            this.$http
                .get('api/bairros.php?id_cidade=' + value.value)
                .then(function (response) {
                    if (response.data) {
                        this.bairros = [];
                        $.each(response.data, function(id, value) {
                            this.bairros.push({ label: value, value: parseInt(id) });
                        }.bind(this));

                        // Se mudou de uma cidade para outra cidade e não é a primeira vez que carrega,
                        // atualiza o bairro para 'Todos', se não, pega o bairro do parâmetro na url
                        if (oldValue.value && oldValue.value !== value.value) {
                        	this.params.bairro = this.bairros[0].value;
                        } else {
                        	this.params.bairro = this.bairro;
                        }

                    }
                });
        }
    },
    created: function() {
    	this.params.finalidade = this.finalidade;
    	this.params.tipo = this.tipo;

        this.$http
                .get('api/cidades.php')
                .then(function (response) {
                    if (response.data) {
                        this.cidades = [];
                        $.each(response.data, function(id, value) {
                            this.cidades.push({ label: value, value: parseInt(id) });
                        }.bind(this));
                        this.params.cidade = this.cidade;
                    }
                });
    }
});
