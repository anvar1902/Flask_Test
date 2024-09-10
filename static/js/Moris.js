
//console.log(data)

Morris.Line({
  //Контейнер для вывода графика
  element: 'myfirstchart',
  //Данные для графика
  data: [
      { date: '2008', hashrate: 144},
      { date: '2009', hashrate: 41},
      { date: '2010', hashrate: 80}
  ],
  xkey: 'date',

  //Префикс в конце для оси Y
  postUnits:' H/s',

  //Коридор цены за 1 доллар
  goals:[45.0, 27.0],
  goalStrokeWidth:2,
  goalLineColors:['#d9534f'],

  //Событийные линии по оси X
  events: ['2014-01-01', '2015-10-01'],
  eventStrokeWidth:2,
  eventLineColors:['#428bca'],

  //Цвет линий
  lineColors:['#5cb85c','#f0ad4e'],
  //Выводимые линии
  ykeys: ["hashrate"],
  //Названия линий
  labels: ['Хэшрейт']
});