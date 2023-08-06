# Generated from C:/Users/ellio/Documents/GitHub/LIE/LIE++\fodcat.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .fodcatParser import fodcatParser
else:
    from fodcatParser import fodcatParser

# This class defines a complete listener for a parse tree produced by fodcatParser.
class fodcatListener(ParseTreeListener):

    # Enter a parse tree produced by fodcatParser#program.
    def enterProgram(self, ctx:fodcatParser.ProgramContext):
        pass

    # Exit a parse tree produced by fodcatParser#program.
    def exitProgram(self, ctx:fodcatParser.ProgramContext):
        pass


    # Enter a parse tree produced by fodcatParser#main_function.
    def enterMain_function(self, ctx:fodcatParser.Main_functionContext):
        pass

    # Exit a parse tree produced by fodcatParser#main_function.
    def exitMain_function(self, ctx:fodcatParser.Main_functionContext):
        pass


    # Enter a parse tree produced by fodcatParser#command.
    def enterCommand(self, ctx:fodcatParser.CommandContext):
        pass

    # Exit a parse tree produced by fodcatParser#command.
    def exitCommand(self, ctx:fodcatParser.CommandContext):
        pass


    # Enter a parse tree produced by fodcatParser#ifstat.
    def enterIfstat(self, ctx:fodcatParser.IfstatContext):
        pass

    # Exit a parse tree produced by fodcatParser#ifstat.
    def exitIfstat(self, ctx:fodcatParser.IfstatContext):
        pass


    # Enter a parse tree produced by fodcatParser#elsestat.
    def enterElsestat(self, ctx:fodcatParser.ElsestatContext):
        pass

    # Exit a parse tree produced by fodcatParser#elsestat.
    def exitElsestat(self, ctx:fodcatParser.ElsestatContext):
        pass


    # Enter a parse tree produced by fodcatParser#func_call.
    def enterFunc_call(self, ctx:fodcatParser.Func_callContext):
        pass

    # Exit a parse tree produced by fodcatParser#func_call.
    def exitFunc_call(self, ctx:fodcatParser.Func_callContext):
        pass


    # Enter a parse tree produced by fodcatParser#flow_exp.
    def enterFlow_exp(self, ctx:fodcatParser.Flow_expContext):
        pass

    # Exit a parse tree produced by fodcatParser#flow_exp.
    def exitFlow_exp(self, ctx:fodcatParser.Flow_expContext):
        pass


    # Enter a parse tree produced by fodcatParser#assignment.
    def enterAssignment(self, ctx:fodcatParser.AssignmentContext):
        pass

    # Exit a parse tree produced by fodcatParser#assignment.
    def exitAssignment(self, ctx:fodcatParser.AssignmentContext):
        pass


    # Enter a parse tree produced by fodcatParser#gpio.
    def enterGpio(self, ctx:fodcatParser.GpioContext):
        pass

    # Exit a parse tree produced by fodcatParser#gpio.
    def exitGpio(self, ctx:fodcatParser.GpioContext):
        pass


    # Enter a parse tree produced by fodcatParser#sleep.
    def enterSleep(self, ctx:fodcatParser.SleepContext):
        pass

    # Exit a parse tree produced by fodcatParser#sleep.
    def exitSleep(self, ctx:fodcatParser.SleepContext):
        pass


    # Enter a parse tree produced by fodcatParser#expression.
    def enterExpression(self, ctx:fodcatParser.ExpressionContext):
        pass

    # Exit a parse tree produced by fodcatParser#expression.
    def exitExpression(self, ctx:fodcatParser.ExpressionContext):
        pass


    # Enter a parse tree produced by fodcatParser#arithmetic_exp.
    def enterArithmetic_exp(self, ctx:fodcatParser.Arithmetic_expContext):
        pass

    # Exit a parse tree produced by fodcatParser#arithmetic_exp.
    def exitArithmetic_exp(self, ctx:fodcatParser.Arithmetic_expContext):
        pass


    # Enter a parse tree produced by fodcatParser#relational_exp.
    def enterRelational_exp(self, ctx:fodcatParser.Relational_expContext):
        pass

    # Exit a parse tree produced by fodcatParser#relational_exp.
    def exitRelational_exp(self, ctx:fodcatParser.Relational_expContext):
        pass


    # Enter a parse tree produced by fodcatParser#logic_exp.
    def enterLogic_exp(self, ctx:fodcatParser.Logic_expContext):
        pass

    # Exit a parse tree produced by fodcatParser#logic_exp.
    def exitLogic_exp(self, ctx:fodcatParser.Logic_expContext):
        pass


    # Enter a parse tree produced by fodcatParser#array_call.
    def enterArray_call(self, ctx:fodcatParser.Array_callContext):
        pass

    # Exit a parse tree produced by fodcatParser#array_call.
    def exitArray_call(self, ctx:fodcatParser.Array_callContext):
        pass


    # Enter a parse tree produced by fodcatParser#function_declaration.
    def enterFunction_declaration(self, ctx:fodcatParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by fodcatParser#function_declaration.
    def exitFunction_declaration(self, ctx:fodcatParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by fodcatParser#array_declaration.
    def enterArray_declaration(self, ctx:fodcatParser.Array_declarationContext):
        pass

    # Exit a parse tree produced by fodcatParser#array_declaration.
    def exitArray_declaration(self, ctx:fodcatParser.Array_declarationContext):
        pass


    # Enter a parse tree produced by fodcatParser#gpio_declaration.
    def enterGpio_declaration(self, ctx:fodcatParser.Gpio_declarationContext):
        pass

    # Exit a parse tree produced by fodcatParser#gpio_declaration.
    def exitGpio_declaration(self, ctx:fodcatParser.Gpio_declarationContext):
        pass


    # Enter a parse tree produced by fodcatParser#parameters_declaration.
    def enterParameters_declaration(self, ctx:fodcatParser.Parameters_declarationContext):
        pass

    # Exit a parse tree produced by fodcatParser#parameters_declaration.
    def exitParameters_declaration(self, ctx:fodcatParser.Parameters_declarationContext):
        pass


    # Enter a parse tree produced by fodcatParser#parameters_called.
    def enterParameters_called(self, ctx:fodcatParser.Parameters_calledContext):
        pass

    # Exit a parse tree produced by fodcatParser#parameters_called.
    def exitParameters_called(self, ctx:fodcatParser.Parameters_calledContext):
        pass


    # Enter a parse tree produced by fodcatParser#int_literal.
    def enterInt_literal(self, ctx:fodcatParser.Int_literalContext):
        pass

    # Exit a parse tree produced by fodcatParser#int_literal.
    def exitInt_literal(self, ctx:fodcatParser.Int_literalContext):
        pass


    # Enter a parse tree produced by fodcatParser#bool_literal.
    def enterBool_literal(self, ctx:fodcatParser.Bool_literalContext):
        pass

    # Exit a parse tree produced by fodcatParser#bool_literal.
    def exitBool_literal(self, ctx:fodcatParser.Bool_literalContext):
        pass


    # Enter a parse tree produced by fodcatParser#float_literal.
    def enterFloat_literal(self, ctx:fodcatParser.Float_literalContext):
        pass

    # Exit a parse tree produced by fodcatParser#float_literal.
    def exitFloat_literal(self, ctx:fodcatParser.Float_literalContext):
        pass


    # Enter a parse tree produced by fodcatParser#strg.
    def enterStrg(self, ctx:fodcatParser.StrgContext):
        pass

    # Exit a parse tree produced by fodcatParser#strg.
    def exitStrg(self, ctx:fodcatParser.StrgContext):
        pass


    # Enter a parse tree produced by fodcatParser#constant.
    def enterConstant(self, ctx:fodcatParser.ConstantContext):
        pass

    # Exit a parse tree produced by fodcatParser#constant.
    def exitConstant(self, ctx:fodcatParser.ConstantContext):
        pass


    # Enter a parse tree produced by fodcatParser#relational_op.
    def enterRelational_op(self, ctx:fodcatParser.Relational_opContext):
        pass

    # Exit a parse tree produced by fodcatParser#relational_op.
    def exitRelational_op(self, ctx:fodcatParser.Relational_opContext):
        pass


    # Enter a parse tree produced by fodcatParser#logic_op.
    def enterLogic_op(self, ctx:fodcatParser.Logic_opContext):
        pass

    # Exit a parse tree produced by fodcatParser#logic_op.
    def exitLogic_op(self, ctx:fodcatParser.Logic_opContext):
        pass


    # Enter a parse tree produced by fodcatParser#arithmetic_op.
    def enterArithmetic_op(self, ctx:fodcatParser.Arithmetic_opContext):
        pass

    # Exit a parse tree produced by fodcatParser#arithmetic_op.
    def exitArithmetic_op(self, ctx:fodcatParser.Arithmetic_opContext):
        pass


    # Enter a parse tree produced by fodcatParser#print_op.
    def enterPrint_op(self, ctx:fodcatParser.Print_opContext):
        pass

    # Exit a parse tree produced by fodcatParser#print_op.
    def exitPrint_op(self, ctx:fodcatParser.Print_opContext):
        pass


    # Enter a parse tree produced by fodcatParser#sign.
    def enterSign(self, ctx:fodcatParser.SignContext):
        pass

    # Exit a parse tree produced by fodcatParser#sign.
    def exitSign(self, ctx:fodcatParser.SignContext):
        pass


    # Enter a parse tree produced by fodcatParser#func_button.
    def enterFunc_button(self, ctx:fodcatParser.Func_buttonContext):
        pass

    # Exit a parse tree produced by fodcatParser#func_button.
    def exitFunc_button(self, ctx:fodcatParser.Func_buttonContext):
        pass


    # Enter a parse tree produced by fodcatParser#func_led.
    def enterFunc_led(self, ctx:fodcatParser.Func_ledContext):
        pass

    # Exit a parse tree produced by fodcatParser#func_led.
    def exitFunc_led(self, ctx:fodcatParser.Func_ledContext):
        pass


    # Enter a parse tree produced by fodcatParser#func_servo.
    def enterFunc_servo(self, ctx:fodcatParser.Func_servoContext):
        pass

    # Exit a parse tree produced by fodcatParser#func_servo.
    def exitFunc_servo(self, ctx:fodcatParser.Func_servoContext):
        pass


    # Enter a parse tree produced by fodcatParser#identifier.
    def enterIdentifier(self, ctx:fodcatParser.IdentifierContext):
        pass

    # Exit a parse tree produced by fodcatParser#identifier.
    def exitIdentifier(self, ctx:fodcatParser.IdentifierContext):
        pass



del fodcatParser