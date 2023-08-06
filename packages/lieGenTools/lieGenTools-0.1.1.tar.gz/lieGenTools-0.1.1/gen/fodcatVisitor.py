# Generated from C:/Users/ellio/Documents/GitHub/LIE/LIE++\fodcat.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .fodcatParser import fodcatParser
else:
    from fodcatParser import fodcatParser

# This class defines a complete generic visitor for a parse tree produced by fodcatParser.

class fodcatVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by fodcatParser#program.
    def visitProgram(self, ctx:fodcatParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#main_function.
    def visitMain_function(self, ctx:fodcatParser.Main_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#command.
    def visitCommand(self, ctx:fodcatParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#ifstat.
    def visitIfstat(self, ctx:fodcatParser.IfstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#elsestat.
    def visitElsestat(self, ctx:fodcatParser.ElsestatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#func_call.
    def visitFunc_call(self, ctx:fodcatParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#flow_exp.
    def visitFlow_exp(self, ctx:fodcatParser.Flow_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#assignment.
    def visitAssignment(self, ctx:fodcatParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#gpio.
    def visitGpio(self, ctx:fodcatParser.GpioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#sleep.
    def visitSleep(self, ctx:fodcatParser.SleepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#expression.
    def visitExpression(self, ctx:fodcatParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#arithmetic_exp.
    def visitArithmetic_exp(self, ctx:fodcatParser.Arithmetic_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#relational_exp.
    def visitRelational_exp(self, ctx:fodcatParser.Relational_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#logic_exp.
    def visitLogic_exp(self, ctx:fodcatParser.Logic_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#array_call.
    def visitArray_call(self, ctx:fodcatParser.Array_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#function_declaration.
    def visitFunction_declaration(self, ctx:fodcatParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#array_declaration.
    def visitArray_declaration(self, ctx:fodcatParser.Array_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#gpio_declaration.
    def visitGpio_declaration(self, ctx:fodcatParser.Gpio_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#parameters_declaration.
    def visitParameters_declaration(self, ctx:fodcatParser.Parameters_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#parameters_called.
    def visitParameters_called(self, ctx:fodcatParser.Parameters_calledContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#int_literal.
    def visitInt_literal(self, ctx:fodcatParser.Int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#bool_literal.
    def visitBool_literal(self, ctx:fodcatParser.Bool_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#float_literal.
    def visitFloat_literal(self, ctx:fodcatParser.Float_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#strg.
    def visitStrg(self, ctx:fodcatParser.StrgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#constant.
    def visitConstant(self, ctx:fodcatParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#relational_op.
    def visitRelational_op(self, ctx:fodcatParser.Relational_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#logic_op.
    def visitLogic_op(self, ctx:fodcatParser.Logic_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#arithmetic_op.
    def visitArithmetic_op(self, ctx:fodcatParser.Arithmetic_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#print_op.
    def visitPrint_op(self, ctx:fodcatParser.Print_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#sign.
    def visitSign(self, ctx:fodcatParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#func_button.
    def visitFunc_button(self, ctx:fodcatParser.Func_buttonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#func_led.
    def visitFunc_led(self, ctx:fodcatParser.Func_ledContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#func_servo.
    def visitFunc_servo(self, ctx:fodcatParser.Func_servoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fodcatParser#identifier.
    def visitIdentifier(self, ctx:fodcatParser.IdentifierContext):
        return self.visitChildren(ctx)



del fodcatParser