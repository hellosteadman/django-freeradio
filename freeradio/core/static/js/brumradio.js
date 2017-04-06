jQuery(document).ready(
    function($) {
        var poll = function() {
            $.getJSON(
                window.RADIO_NOWPLAYING_URL + '&callback=?',
                function(data) {
                    for(var i = 0; i < data.data.length; i ++) {
                        $('.now-playing').addClass('active').find('.song').text(
                            data.data[i].song
                        );
                    }
                }
            );
        };

        setInterval(poll, 15 * 1000);
        poll();

        $('[data-action="toggle-player"]').on('click',
            function() {
                var container = $('#player-container');
                var player = videojs('player');

                if(container.hasClass('active')) {
                    container.removeClass('active');
                    player.pause();
                } else {
                    container.addClass('active');
                    player.play();
                }
            }
        );

        $('.infinite-scroll').each(
            function() {
                var self = $(this);
                var infinite = new Waypoint.Infinite(
                    {
                        element: self.get(0)
                    }
                );
            }
        );

        $('.noticeboard').each(
            function() {
                $(this).isotope(
                    {
                        itemSelector: '.notice',
                        layoutMode: 'packery'
                    }
                );
            }
        );

        $('.btn-shares a').on('click',
            function(e) {
                var self = $(this);
                var url = self.attr('href');
                var width = 580;
                var height = 610;
                var left = (window.screen.width / 2) - ((width / 2) + 10);
                var top = (window.screen.height / 2) - ((height / 2) + 50);
                var options = {
                    width: width,
                    height: height,
                    menubar: 'no',
                    status: 'no',
                    left: left,
                    top: top
                };

                if(self.data('action')) {
                    return;
                }

                e.preventDefault();
                var optionsStr = (
                    function() {
                        var pairs = [];

                        for(var k in options) {
                            pairs.push(k + '=' + escape(options[k]));
                        }

                        return pairs.join(',');
                    }
                )();

                window.open(url, 'share', optionsStr);
            }
        );
    }
);
