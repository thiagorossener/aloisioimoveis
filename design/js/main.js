new Vue({
    el: '#search',
    data: {
        finalidade: 'alugar',
        tiposDeImovel: [
            { label: 'Casa', value: 'casa'},
            { label: 'Apartamento', value: 'apartamento'},
            { label: 'Comercial', value: 'comercial'},
            { label: 'Terreno', value: 'terreno'}
        ],
        currentTipoDeImovel: { label: 'Casa', value: 'casa'},
        cidades: [
            { label: 'Todas', value: 'todas'},
            { label: 'Caçapava', value: '9'},
            { label: 'Campos do Jordão', value: '11'},
            { label: 'Lagoinha', value: '7'},
            { label: 'Natividade da Serra', value: '6'},
            { label: 'Pindamonhangaba', value: '8'},
            { label: 'Redenção da Serra', value: '5'},
            { label: 'São José dos Campos', value: '12'},
            { label: 'São Luiz do Paraitinga', value: '4'},
            { label: 'Taubaté', value: '1'},
            { label: 'Tremembé', value: '2'},
            { label: 'Ubatuba', value: '3'}
        ],
        currentCidade: { label: 'Taubaté', value: '1'},
        bairros: [
            { label: 'Todos os bairros', value: 'todos'},
            { label: 'Belém', value: '1'},
            { label: 'Independência', value: '2'}
        ],
        currentBairro: { label: 'Todos os bairros', value: 'todos'},
        searchForFicha: false
    },
    methods: {
        setFinalidade: function(finalidade) {
            this.finalidade = finalidade;
        },
        setTipoDeImovel: function(tipoDeImovel) {
            this.currentTipoDeImovel = tipoDeImovel;
        },
        setCidade: function(cidade) {
            this.currentCidade = cidade;
        },
        setBairro: function(bairro) {
            this.currentBairro = bairro;
        }
    }
});
