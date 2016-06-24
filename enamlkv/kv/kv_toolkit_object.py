#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Typed

from enaml.widgets.toolkit_object import ProxyToolkitObject

from kivy.uix.widget import WidgetBase
from kivy.event import EventDispatcher

#class KvToolkitObjectMeta(type(ProxyToolkitObject),type(EventDispatcher)):
#    pass 

class KvToolkitObject(ProxyToolkitObject):
    """ A Kv implementation of an Enaml ProxyToolkitObject.

    """
    __slots__ = '__weakref__'
    
    #__metaclass__ = KvToolkitObjectMeta
    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(WidgetBase)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = WidgetBase()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        print("KvToolkitObject.init_widget({})".format(self))
        widget = self.widget
        if widget is not None:
            # Each Kv object gets a name. If one is not provided by the
            # widget author, one is generated. This is required so that
            # Kv stylesheet cascading can be prevented (Enaml's styling
            # engine applies the cascade itself). Names provided by the
            # widget author are assumed to be unique.
            d = self.declaration
            name = d.name or u'obj-%d' % id(d)
            widget.id = name
            parent = self.parent_widget()
            if parent:
                parent.add_widget(widget)
            #    print("YO: {}.parent = {}".format(widget,self.parent_widget()))

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        pass

    #--------------------------------------------------------------------------
    # ProxyToolkitObject API
    #--------------------------------------------------------------------------
    def activate_top_down(self):
        """ Activate the proxy for the top-down pass.

        """
        self.create_widget()
        self.init_widget()

    def activate_bottom_up(self):
        """ Activate the proxy tree for the bottom-up pass.

        """
        self.init_layout()

    def destroy(self):
        """ A reimplemented destructor.

        This destructor will clear the reference to the toolkit widget
        and set its parent to None.

        """
        widget = self.widget
        if widget is not None:
            widget.parent = None
            del self.widget
        super(KvToolkitObject, self).destroy()

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(KvToolkitObject, self).child_removed(child)
        if child.widget is not None:
            child.widget.parent = None

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def parent_widget(self):
        """ Get the parent toolkit widget for this object.

        Returns
        -------
        result : QObject or None
            The toolkit widget declared on the declaration parent, or
            None if there is no such parent.

        """
        parent = self.parent()
        if parent is not None:
            return parent.widget

    def child_widgets(self):
        """ Get the child toolkit widgets for this object.

        Returns
        -------
        result : iterable of QObject
            The child widgets defined for this object.

        """
        for child in self.children():
            w = child.widget
            if w is not None:
                yield w