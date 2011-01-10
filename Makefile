PREFIX=/usr
PROGRAMS=pycat.py \
         pycatconf.py \
		 pycatgui.py

all:

install: $(PROGRAMS)
	if test -d $(PREFIX)/share/pycat; \
	then \
		rm -rf $(PREFIX)/share/pycat; \
	fi
	mkdir -p $(PREFIX)/share/pycat/data
	for i in data/*; do \
		cp $$i $(PREFIX)/share/pycat/data; \
	done
	cp pycat.desktop /usr/share/applications
	for i in $(PROGRAMS); do \
		n=`basename $$i .py`; \
		if test -L $(PREFIX)/bin/$$n; \
		then \
			rm -f $(PREFIX)/bin/$$n; \
		fi; \
		cp $$i $(PREFIX)/share/pycat; \
		chmod 755 $(PREFIX)/share/pycat/$$i; \
		ln -s $(PREFIX)/share/pycat/$$i $(PREFIX)/bin/$$n; \
	done

uninstall:
	for i in $(PROGRAMS); do \
		n=`basename $$i .py`; \
		if test -e $(PREFIX)/bin/$$n; \
		then \
			rm -f $(PREFIX)/bin/$$n; \
		fi; \
	done
	if test -d $(PREFIX)/share/pycat; \
	then \
		rm -rf $(PREFIX)/share/pycat; \
	fi
	if test -f /usr/share/applications/pycat.desktop; \
	then \
		rm /usr/share/applications/pycat.desktop; \
	fi
clean:
	rm -f *.pyc
